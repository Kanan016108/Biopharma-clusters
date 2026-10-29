
from typing import Literal, Optional   
from dataclasses import dataclass, field

# Label = "biotech"/ "pharma"    Enumeration (2 named values)
# Labels come from the ETF the ticker symbol was in 
# Main used are ETF'S are XBI,IBB ,PPH,XPH 
#This is our substitute for the GICS sub-industry 

label= Literal ["biotech","pharma"]
LABELS = ("biotech", "pharma")







#-------
#company = (ticker,name,label)
#examples = Company("VRTX", "Vertex pharmaceuticals", "biotech")
#-------

@dataclass(frozen=True)
class company:
    ticker:str
    name:str
    label:label
#-----
#fundamentals = one company in fiscal year, 13 features after scaling 
#Scaling rule:
#    log fields -> ln(raw) - Applies the natural logarithm to raw assest and share counts 
#    ratio fields -> raw/total assests - divides ten financial line items (like R&D, cash, or debt) by total_assets
#z fields -> standardised across the universe in that year 
#          : company age (done later , in to_matrix )
#Number of employees dropped due to potetial look ahead bias
#interval rules :ratio fields are >= 0; log fields need raw > 0 . 
#Example: fundamentals("VRTX",2022,log_assets=23.5, ppe=0.07, ... )

@dataclass(frozen=True)
class Fundamentals:
    ticker:str
    year: int 
    log_assets: float  #1 (total assets)
    ppe : float        #2 PP&e/ assets - captures physical footprint
    intagibles: float  #3 Intangibles/assets- tracks buyers vs builders 
    cash : float       #4 cash/assets- A good metric for runway
    sales : float      #5 sales/assets- do they have a product that generates revenue ?
    advertising : float #6 advertising/assets (0 if not repoerted) - tracks advertising costs 
    rnd : float         #7 R&D/assets - measures research intensity 
    capex: float        #8 capex/assets  
    dividends : float   #9 cash dividends/assets
    log_shares: float   #10 lm(common shares outstanding)
    debt_issued: float  #11 long-term debt issues/ assets
    total_debt: float   # total debt /assets
    age: float          # company age in years (raw; z -score later)

FEATURE_NAMES = [
"log_assets","ppe","intangibles","cash","sales","advertising",
"rnd","capex","dividends","log_shares","debt_issued", "total_debt",
"age",
]

#-------
#phase = one of six development stages
#--------
phase= Literal["preclinical", "phase1","phase2","phase3","nda_bla","approved"]
PHASES = ("preclinical", "phase1","phase2","phase3","nda_bla","approved")


#-------
#indication = one of twenty therapeutica groups 
#-------
INDICATIONS = (
    "Allergy", "Autoimmune/immunology", "Cardiovascular", "Dermatology",
    "ENT/Dental", "Endocrine", "Gastroenterology", "Hematology",
    "Infectious Disease", "Metabolic", "Neurology", "Obstetrics/Gynecology",
    "Oncology", "Ophthalmology", "Orthopedics", "Psychiatry", "Renal",
    "Respiratory", "Rheumatology", "Urology",
)
inidcation = str # must be one of INDICATIONS 


#-------------
#Trial= (phase, indication)
#one clinical trial record after cleaning. 
#phase tells use the phase of the drug cycle 
#inidaction tells us the therapeutic category, must be one of the indications 
#-------------
@dataclass(frozen=True)
class trial:
    phase:optional[phase]    
    indication:Optional[Indication]

#-------------
# Pipeline = {ticker, year, phase_counts, indication_share}   Structure
#   phase_counts     : dict[Phase, int]        how many drugs in each stage
#   indication_share : dict[Indication, float] fraction of drugs per group,
#                      shares sum to 1.0 (or dict is empty if no drugs)
# Rules carried by this definition (Xu, Section 2.2.3):
#   INDICATION_CUTOFF = 0.75  -> a company "belongs" to a group only if at
#                                least 75% of its drugs are in that group
#   SIZE_PERCENTILE   = 75    -> Big = total assets >= 75th percentile
#--------------
INDCATION_CUTOFF= 0.75 
SIZE_PERCENTILE= 75 

dataclass
class pipeline:
    ticker: str 
    year:int 
    pahse_counts: dict= field(default_factory=dict)
    indication_share:dict= field(default_factory=dict)