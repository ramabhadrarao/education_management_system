# seed_data.py
from app import create_app, db
from app.domain.models.faculty_details import LookupTable

def seed_lookup_tables():
    # Publication Types
    publication_types = [
        {'lookup_type': 'publication_type', 'lookup_value': 'Journal Article'},
        {'lookup_type': 'publication_type', 'lookup_value': 'Conference Paper'},
        {'lookup_type': 'publication_type', 'lookup_value': 'Book Chapter'},
        {'lookup_type': 'publication_type', 'lookup_value': 'Book'},
        {'lookup_type': 'publication_type', 'lookup_value': 'Patent'}
    ]
    
    # Workshop Types
    workshop_types = [
        {'lookup_type': 'workshop_type', 'lookup_value': 'Workshop'},
        {'lookup_type': 'workshop_type', 'lookup_value': 'Seminar'},
        {'lookup_type': 'workshop_type', 'lookup_value': 'Conference'},
        {'lookup_type': 'workshop_type', 'lookup_value': 'Symposium'}
    ]
    
    # FDP Types
    fdp_types = [
        {'lookup_type': 'fdp_type', 'lookup_value': 'Faculty Development Program'},
        {'lookup_type': 'fdp_type', 'lookup_value': 'Management Development Program'},
        {'lookup_type': 'fdp_type', 'lookup_value': 'Short Term Training Program'},
        {'lookup_type': 'fdp_type', 'lookup_value': 'Orientation Program'}
    ]
    
    # Award Categories
    award_categories = [
        {'lookup_type': 'award_category', 'lookup_value': 'Teaching Excellence'},
        {'lookup_type': 'award_category', 'lookup_value': 'Research Excellence'},
        {'lookup_type': 'award_category', 'lookup_value': 'Service Excellence'},
        {'lookup_type': 'award_category', 'lookup_value': 'Lifetime Achievement'}
    ]
    
    # Funding Agencies
    funding_agencies = [
        {'lookup_type': 'funding_agency', 'lookup_value': 'UGC'},
        {'lookup_type': 'funding_agency', 'lookup_value': 'AICTE'},
        {'lookup_type': 'funding_agency', 'lookup_value': 'DST'},
        {'lookup_type': 'funding_agency', 'lookup_value': 'CSIR'},
        {'lookup_type': 'funding_agency', 'lookup_value': 'DBT'},
        {'lookup_type': 'funding_agency', 'lookup_value': 'Industry Sponsored'}
    ]
    
    # Leave Types
    leave_types = [
        {'lookup_type': 'leave_type', 'lookup_value': 'Casual Leave'},
        {'lookup_type': 'leave_type', 'lookup_value': 'Medical Leave'},
        {'lookup_type': 'leave_type', 'lookup_value': 'Earned Leave'},
        {'lookup_type': 'leave_type', 'lookup_value': 'On Duty'},
        {'lookup_type': 'leave_type', 'lookup_value': 'Study Leave'}
    ]
    
    # Combine all lookup data
    all_lookups = publication_types + workshop_types + fdp_types + award_categories + funding_agencies + leave_types
    
    # Add to database
    for lookup_data in all_lookups:
        # Check if already exists
        existing = LookupTable.query.filter_by(
            lookup_type=lookup_data['lookup_type'],
            lookup_value=lookup_data['lookup_value']
        ).first()
        
        if not existing:
            lookup = LookupTable(**lookup_data)
            db.session.add(lookup)
    
    db.session.commit()
    print("Lookup tables seeded successfully!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_lookup_tables()