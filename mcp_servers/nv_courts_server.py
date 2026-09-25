#!/usr/bin/env python3
"""
MCP Server: Nevada Courts Information

Provides NYE County District Court procedures and rules.
"""

import json
from typing import Dict, List, Any


class NVCourtsServer:
    """Nevada courts information server"""
    
    NYE_COUNTY_DISTRICT_COURT = {
        'name': 'Nye County District Court',
        'address': '2100 E Main St, Pahrump, NV 89060',
        'phone': '(775) 751-7000',
        'website': 'https://www.nyecourts.us',
        'clerk_email': 'clerk@nyecourts.us',
        'hours': 'Monday-Friday, 8:00 AM - 5:00 PM',
    }
    
    JUDGES = {
        'District Court': [
            {'name': 'Judge [Name]', 'division': 'Criminal', 'phone': '(775) 751-7000'},
        ]
    }
    
    LOCAL_RULES = {
        'criminal': {
            'filing_fees': 'See clerk',
            'motion_deadline_before_trial': '14 days',
            'discovery_requirements': 'Nevada Rules of Criminal Procedure',
            'plea_procedures': 'Judge approval required',
            'sentencing_considerations': 'Nevada Sentencing Guidelines',
        },
        'civil': {
            'filing_fees': 'Varies by case type',
            'motion_deadlines': '21 days before trial',
            'discovery_limits': 'Nevada Rules of Civil Procedure',
            'summary_judgment': 'Supported',
        }
    }
    
    def get_court_info(self) -> Dict[str, Any]:
        """Get Nye County District Court info"""
        return self.NYE_COUNTY_DISTRICT_COURT
    
    def get_judges(self, division: str = "Criminal") -> List[Dict[str, str]]:
        """Get judges by division"""
        return self.JUDGES.get('District Court', [])
    
    def get_filing_procedures(self, case_type: str = "criminal") -> Dict[str, Any]:
        """Get filing procedures"""
        return self.LOCAL_RULES.get(case_type, {})
    
    def get_statute_of_limitations(self, offense: str, state: str = "Nevada") -> Dict[str, Any]:
        """Get statute of limitations"""
        limitations = {
            'criminal_felony': {'years': 3, 'description': 'Most felonies'},
            'criminal_misdemeanor': {'years': 2, 'description': 'Misdemeanors'},
            'section_1983_federal': {'years': 3, 'description': 'Civil rights suits'},
            'state_tort': {'years': 2, 'description': 'Torts under Nevada law'},
        }
        return limitations.get(offense, {})
    
    def get_contact_info(self, office: str) -> Dict[str, str]:
        """Get contact info for court offices"""
        offices = {
            'Clerk of Court': {
                'address': '2100 E Main St, Pahrump, NV 89060',
                'phone': '(775) 751-7000',
                'email': 'clerk@nyecourts.us',
            },
            'District Attorney': {
                'address': '2100 E Main St, Pahrump, NV 89060',
                'phone': '(775) 751-7000',
                'website': 'https://www.nyecounty.us/da',
            },
            'Public Defender': {
                'address': '2100 E Main St, Pahrump, NV 89060',
                'phone': '(775) 751-7000',
            },
        }
        return offices.get(office, {})


if __name__ == "__main__":
    server = NVCourtsServer()
    print(json.dumps(server.get_court_info(), indent=2))
    print(json.dumps(server.get_filing_procedures(), indent=2))
