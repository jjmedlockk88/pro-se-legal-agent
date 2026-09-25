#!/usr/bin/env python3
"""
Pro Se Legal Assistant Agent - Main Orchestrator

Handles:
- LLM interaction (local Ollama models)
- Skill invocation (criminal defense, civil rights)
- MCP server communication
- Case state management
- Workflow orchestration

Designed for NYE County, Nevada pro se defendants
"""

import os
import sys
import json
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
import yaml

from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema import LLMResult
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from mcp import ClientSession, StdioServerParameters
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class CaseInfo:
    """Represents a legal case"""
    case_name: str
    case_number: str
    jurisdiction: str = "Nye County, Nevada"
    case_type: str = "criminal"  # criminal or civil_rights
    charges: Optional[List[str]] = None
    defendant_name: str = ""
    attorney: str = "Pro Se"
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class OllamaLLM(LLM):
    """Custom LLM class for Ollama integration"""
    
    model: str = "mistral:7b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.3
    max_tokens: int = 2000
    
    @property
    def _llm_type(self) -> str:
        return "ollama"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        import requests
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                    "stop": stop,
                },
                stream=False,
                timeout=60,
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            raise


class ProSeLegalAgent:
    """Main agent for pro se legal assistance"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize agent with configuration"""
        self.config = self._load_config(config_path)
        self.llm = self._init_llm()
        self.case: Optional[CaseInfo] = None
        self.memory: Dict[str, Any] = {}
        self.mcp_sessions = {}
        
        logger.info("Pro Se Legal Agent initialized")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load YAML configuration"""
        if not os.path.exists(config_path):
            logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return {}
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _init_llm(self) -> OllamaLLM:
        """Initialize Ollama LLM"""
        llm_config = self.config.get('llm', {})
        return OllamaLLM(
            model=llm_config.get('model', 'mistral:7b'),
            base_url=llm_config.get('base_url', 'http://localhost:11434'),
            temperature=llm_config.get('temperature', 0.3),
            max_tokens=llm_config.get('max_tokens', 2000),
        )
    
    def set_case(self, case: CaseInfo):
        """Set current case"""
        self.case = case
        self.memory['current_case'] = asdict(case)
        logger.info(f"Case set: {case.case_name} ({case.case_number})")
    
    def task(self, user_query: str) -> str:
        """
        Main task execution method.
        
        Routes query to appropriate skill based on content.
        """
        logger.info(f"Task: {user_query[:100]}...")
        
        # Determine task type
        task_type = self._classify_task(user_query)
        logger.info(f"Task type: {task_type}")
        
        # Route to appropriate skill
        if task_type == "criminal":
            return self._handle_criminal_task(user_query)
        elif task_type == "civil_rights":
            return self._handle_civil_rights_task(user_query)
        elif task_type == "research":
            return self._handle_research_task(user_query)
        else:
            return self._handle_general_task(user_query)
    
    def _classify_task(self, query: str) -> str:
        """Classify task type based on keywords"""
        query_lower = query.lower()
        
        # Civil rights keywords
        if any(kw in query_lower for kw in ['1983', 'civil rights', 'monell', 'constitutional', 'police abuse']):
            return "civil_rights"
        
        # Criminal keywords
        if any(kw in query_lower for kw in ['criminal', 'arrest', 'charges', 'plea', 'conviction', 'motion to suppress', 'evidence']):
            return "criminal"
        
        # Research keywords
        if any(kw in query_lower for kw in ['research', 'case law', 'statute', 'ruling', 'precedent', 'what is']):
            return "research"
        
        return "general"
    
    def _handle_criminal_task(self, query: str) -> str:
        """Handle criminal defense tasks"""
        prompt_template = PromptTemplate(
            input_variables=["case_info", "query"],
            template="""
You are a legal research assistant helping a pro se criminal defendant in {case_info}.

Context: Nevada Rules of Criminal Procedure, Nye County District Court procedures.

User Query: {query}

Provide:
1. Relevant Nevada statutes and case law
2. Specific legal strategy
3. Motion/pleading suggestions
4. Deadlines and procedural requirements
5. Evidence considerations (Brady, Giglio)

Be precise and cite applicable law.
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        case_info = json.dumps(asdict(self.case) if self.case else {}, indent=2)
        
        try:
            response = chain.run(case_info=case_info, query=query)
            return response
        except Exception as e:
            logger.error(f"Criminal task error: {e}")
            return f"Error processing criminal task: {e}"
    
    def _handle_civil_rights_task(self, query: str) -> str:
        """Handle §1983 Monell civil rights tasks"""
        prompt_template = PromptTemplate(
            input_variables=["case_info", "query"],
            template="""
You are a legal research assistant helping a pro se plaintiff in a 42 USC §1983 civil rights case.

Jurisdiction: Nye County, Nevada. Federal jurisdiction: District Court of Nevada, 9th Circuit.

Your expertise:
- Monell municipal liability doctrine
- Policy and custom analysis
- §1983 standing and elements
- 9th Circuit qualified immunity standards
- Damages calculation under §1983

User Query: {query}

Provide:
1. Applicable §1983 and Monell principles
2. Factual elements needed for success
3. Policy/custom discovery strategy
4. Relevant case law (9th Circuit, Supreme Court)
5. Damage calculation guidance
6. Municipal immunity defenses and responses

Be specific and cite recent case law.
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        case_info = json.dumps(asdict(self.case) if self.case else {}, indent=2)
        
        try:
            response = chain.run(case_info=case_info, query=query)
            return response
        except Exception as e:
            logger.error(f"Civil rights task error: {e}")
            return f"Error processing civil rights task: {e}"
    
    def _handle_research_task(self, query: str) -> str:
        """Handle legal research tasks"""
        prompt_template = PromptTemplate(
            input_variables=["query"],
            template="""
You are a legal research assistant. Provide comprehensive, well-cited legal research.

Query: {query}

Provide:
1. Current state of the law
2. Landmark cases (Supreme Court, Circuit)
3. Recent developments
4. Practical application
5. Citations to statutes and cases

Be thorough and cite all sources.
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        try:
            response = chain.run(query=query)
            return response
        except Exception as e:
            logger.error(f"Research task error: {e}")
            return f"Error processing research task: {e}"
    
    def _handle_general_task(self, query: str) -> str:
        """Handle general queries"""
        try:
            response = self.llm(query)
            return response
        except Exception as e:
            logger.error(f"General task error: {e}")
            return f"Error processing query: {e}"


def main():
    """CLI entry point"""
    print("\n=== Pro Se Legal Assistant - NYE County, NV ===")
    print("Free legal research and drafting for criminal defense and civil rights\n")
    
    try:
        agent = ProSeLegalAgent()
        print("✓ Agent initialized successfully\n")
    except Exception as e:
        print(f"✗ Error initializing agent: {e}")
        print("Make sure Ollama is running: ollama serve")
        sys.exit(1)
    
    # Interactive loop
    while True:
        print("-" * 60)
        user_input = input("\nYour query (or 'quit' to exit):\n> ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nExiting. Good luck with your case.\n")
            break
        
        if not user_input:
            continue
        
        print("\nProcessing...\n")
        response = agent.task(user_input)
        print(response)


if __name__ == "__main__":
    main()
