"""
build_dataset.py
Generates data/schemes.csv — a dataset of Indian government welfare
schemes (Central + all 28 States + 8 UTs) tagged with eligibility
attributes: gender, caste category, income ceiling, age range, state,
occupation and category, used by the recommendation engine.

Scheme names/departments here reflect well-known, publicly documented
Central and State welfare schemes. Benefit amounts change frequently
with each state budget — verify current figures on the official state
portal before citing exact numbers in a report or viva.
"""
import csv

# Columns:
# scheme_id, scheme_name, level (Central/State), state, department,
# category, gender (All/Male/Female/Transgender), caste_category
# (All/SC/ST/OBC/General/Minority), min_age, max_age, max_income (INR/yr,
# -1 = no limit), occupation (All/Farmer/Student/Laborer/Unemployed/
# Self-employed/Woman-headed household/Senior Citizen/Disabled),
# description, benefits, official_link

ROWS = []
sid = [0]

def add(name, level, state, dept, category, gender, caste, min_age, max_age,
        max_income, occupation, description, benefits, link):
    sid[0] += 1
    ROWS.append([
        f"SCH{sid[0]:04d}", name, level, state, dept, category, gender,
        caste, min_age, max_age, max_income, occupation, description,
        benefits, link
    ])

# ---------------------------------------------------------------
# CENTRAL / ALL-INDIA SCHEMES
# ---------------------------------------------------------------
add("PM Kisan Samman Nidhi", "Central", "All India", "Ministry of Agriculture",
    "Agriculture", "All", "All", 18, 100, 200000, "Farmer",
    "Income support for small and marginal farmer families.",
    "Rs 6,000/year in 3 installments of Rs 2,000 each.",
    "https://pmkisan.gov.in")

add("Pradhan Mantri Awas Yojana (Urban)", "Central", "All India",
    "Ministry of Housing and Urban Affairs", "Housing", "All", "All", 18, 100,
    300000, "All", "Interest subsidy on home loans for EWS/LIG/MIG urban households.",
    "Interest subsidy up to Rs 2.67 lakh on home loans.",
    "https://pmaymis.gov.in")

add("Pradhan Mantri Awas Yojana (Gramin)", "Central", "All India",
    "Ministry of Rural Development", "Housing", "All", "All", 18, 100,
    120000, "All", "Financial assistance to build pucca houses for rural poor households.",
    "Rs 1.2 lakh (plain areas) / Rs 1.3 lakh (hilly areas) assistance.",
    "https://pmayg.nic.in")

add("Ayushman Bharat - PMJAY", "Central", "All India", "Ministry of Health & Family Welfare",
    "Health", "All", "All", 0, 100, 500000, "All",
    "Health insurance cover for economically vulnerable families.",
    "Cashless health cover of Rs 5 lakh/family/year.",
    "https://pmjay.gov.in")

add("Pradhan Mantri Ujjwala Yojana", "Central", "All India",
    "Ministry of Petroleum & Natural Gas", "Welfare", "Female", "All", 18, 100,
    100000, "Woman-headed household",
    "Free LPG connections to women from BPL households.",
    "Free LPG gas connection + first refill support.",
    "https://pmuy.gov.in")

add("Pradhan Mantri Jan Dhan Yojana", "Central", "All India",
    "Ministry of Finance", "Financial Inclusion", "All", "All", 10, 100, -1,
    "All", "Universal access to banking with zero-balance accounts.",
    "Zero-balance account, RuPay card, Rs 2 lakh accident insurance.",
    "https://pmjdy.gov.in")

add("Sukanya Samriddhi Yojana", "Central", "All India", "Ministry of Finance",
    "Girl Child", "Female", "All", 0, 10, -1, "All",
    "Small savings scheme for the girl child's education and marriage.",
    "High interest savings account, tax benefits under 80C.",
    "https://www.india.gov.in/sukanya-samriddhi-yojana")

add("Beti Bachao Beti Padhao", "Central", "All India",
    "Ministry of Women & Child Development", "Girl Child", "Female", "All", 0, 18,
    -1, "All", "Awareness and welfare scheme for the survival, protection and education of the girl child.",
    "Educational support, awareness campaigns, incentives.",
    "https://wcd.nic.in/bbbp-schemes")

add("National Old Age Pension Scheme (IGNOAPS)", "Central", "All India",
    "Ministry of Rural Development", "Pension", "All", "All", 60, 100, 100000,
    "Senior Citizen", "Monthly pension for BPL elderly citizens.",
    "Rs 200-500/month (state top-ups vary).",
    "https://nsap.nic.in")

add("Pradhan Mantri Matru Vandana Yojana", "Central", "All India",
    "Ministry of Women & Child Development", "Maternity", "Female", "All", 19, 45,
    -1, "All", "Maternity benefit for pregnant and lactating mothers.",
    "Rs 5,000 cash incentive for first living child.",
    "https://pmmvy.wcd.gov.in")

add("Pradhan Mantri Jeevan Jyoti Bima Yojana", "Central", "All India",
    "Ministry of Finance", "Insurance", "All", "All", 18, 50, -1, "All",
    "Renewable term life insurance for bank account holders.",
    "Rs 2 lakh life cover for Rs 436/year premium.",
    "https://jansuraksha.gov.in")

add("Pradhan Mantri Suraksha Bima Yojana", "Central", "All India",
    "Ministry of Finance", "Insurance", "All", "All", 18, 70, -1, "All",
    "Accidental death and disability insurance scheme.",
    "Rs 2 lakh accident cover for Rs 20/year premium.",
    "https://jansuraksha.gov.in")

add("Atal Pension Yojana", "Central", "All India", "Ministry of Finance",
    "Pension", "All", "All", 18, 40, -1, "Unemployed",
    "Guaranteed pension scheme for unorganized sector workers.",
    "Monthly pension of Rs 1,000-5,000 after age 60.",
    "https://npscra.nsdl.co.in/scheme-details.php")

add("National Scholarship Portal - Post Matric SC", "Central", "All India",
    "Ministry of Social Justice & Empowerment", "Education", "All", "SC", 15, 30,
    250000, "Student", "Scholarship for SC students studying post-matriculation courses.",
    "Full tuition fee + maintenance allowance.",
    "https://scholarships.gov.in")

add("National Scholarship Portal - Post Matric ST", "Central", "All India",
    "Ministry of Tribal Affairs", "Education", "All", "ST", 15, 30, 250000,
    "Student", "Scholarship for ST students studying post-matriculation courses.",
    "Full tuition fee + maintenance allowance.",
    "https://scholarships.gov.in")

add("National Scholarship Portal - Post Matric OBC", "Central", "All India",
    "Ministry of Social Justice & Empowerment", "Education", "All", "OBC", 15, 30,
    150000, "Student", "Scholarship for OBC students studying post-matriculation courses.",
    "Tuition fee reimbursement + maintenance allowance.",
    "https://scholarships.gov.in")

add("Pradhan Mantri Mudra Yojana", "Central", "All India",
    "Ministry of Finance", "Self-Employment", "All", "All", 18, 100, -1, "Self-employed",
    "Collateral-free loans to micro/small enterprises.",
    "Loans up to Rs 10 lakh under Shishu/Kishor/Tarun categories.",
    "https://www.mudra.org.in")

add("Stand-Up India Scheme", "Central", "All India", "Ministry of Finance",
    "Self-Employment", "All", "SC", 18, 100, -1, "Self-employed",
    "Bank loans for SC/ST and women entrepreneurs for greenfield enterprises.",
    "Loans between Rs 10 lakh and Rs 1 crore.",
    "https://www.standupmitra.in")

add("Pradhan Mantri Fasal Bima Yojana", "Central", "All India",
    "Ministry of Agriculture", "Agriculture", "All", "All", 18, 100, -1,
    "Farmer", "Crop insurance scheme protecting farmers against crop loss.",
    "Insurance cover against natural calamities, pests and diseases.",
    "https://pmfby.gov.in")

add("MGNREGA", "Central", "All India", "Ministry of Rural Development",
    "Employment", "All", "All", 18, 100, -1, "Laborer",
    "Guaranteed 100 days of wage employment per year for rural households.",
    "100 days guaranteed wage employment/year.",
    "https://nrega.nic.in")

add("Divyangjan Disability Pension (NSAP)", "Central", "All India",
    "Ministry of Rural Development", "Pension", "All", "All", 18, 79, 100000,
    "Disabled", "Monthly pension for persons with severe disabilities.",
    "Rs 300-500/month (state top-ups vary).",
    "https://nsap.nic.in")

add("PM Vishwakarma Yojana", "Central", "All India", "Ministry of MSME",
    "Self-Employment", "All", "All", 18, 100, -1, "Self-employed",
    "Support for traditional artisans and craftspeople (18 trades).",
    "Toolkit incentive, collateral-free loans up to Rs 3 lakh, skill training.",
    "https://pmvishwakarma.gov.in")

add("National Means-cum-Merit Scholarship", "Central", "All India",
    "Ministry of Education", "Education", "All", "All", 13, 18, 150000, "Student",
    "Scholarship for meritorious students of economically weaker sections.",
    "Rs 12,000/year (classes 9-12).",
    "https://scholarships.gov.in")

add("PM CARES for Children", "Central", "All India",
    "Ministry of Women & Child Development", "Welfare", "All", "All", 0, 23,
    -1, "All", "Support for children who lost parents/guardians to COVID-19.",
    "Education support, health insurance, monthly stipend at 18.",
    "https://pmcaresforchildren.in")

add("Deendayal Antyodaya Yojana - NULM", "Central", "All India",
    "Ministry of Housing and Urban Affairs", "Self-Employment", "All", "All", 18,
    100, 100000, "Unemployed", "Urban poverty alleviation through self-employment and skill training.",
    "Subsidized loans, skill training, shelter for urban homeless.",
    "https://nulm.gov.in")

# ---------------------------------------------------------------
# STATE-SPECIFIC SCHEMES (representative flagship schemes/state)
# ---------------------------------------------------------------
STATE_SCHEMES = [
    # (state, name, dept, category, gender, caste, min_age, max_age, max_income, occ, desc, benefit)
    ("Maharashtra", "Mukhyamantri Majhi Ladki Bahin Yojana", "Women & Child Development",
     "Welfare", "Female", "All", 21, 65, 100000, "Woman-headed household",
     "Monthly financial assistance to eligible women.", "Rs 1,500/month direct benefit transfer."),
    ("Maharashtra", "Rajarshi Chhatrapati Shahu Maharaj Scholarship", "Higher & Technical Education",
     "Education", "All", "SC", 17, 35, 800000, "Student",
     "Tuition and exam fee waiver for professional courses.", "Full tuition & exam fee reimbursement."),
    ("Maharashtra", "Mahatma Jyotirao Phule Jan Arogya Yojana", "Public Health",
     "Health", "All", "All", 0, 100, 100000, "All",
     "Cashless treatment for below-poverty-line families.", "Health cover up to Rs 5 lakh/family/year."),

    ("Karnataka", "Gruha Lakshmi Scheme", "Women & Child Development", "Welfare",
     "Female", "All", 18, 100, 300000, "Woman-headed household",
     "Monthly cash assistance to women heads of BPL households.", "Rs 2,000/month direct benefit transfer."),
    ("Karnataka", "Anna Bhagya Scheme", "Food & Civil Supplies", "Food Security",
     "All", "All", 0, 100, 100000, "All",
     "Free rice distribution to BPL/Antyodaya families.", "10 kg free rice/person/month."),
    ("Karnataka", "Vidyasiri Scholarship", "Backward Classes Welfare", "Education",
     "All", "OBC", 17, 30, 250000, "Student",
     "Hostel/scholarship support for backward class students.", "Monthly maintenance allowance + hostel facility."),

    ("Gujarat", "Mukhyamantri Mahila Utkarsh Yojana", "Women & Child Development",
     "Self-Employment", "Female", "All", 18, 60, 600000, "Self-employed",
     "Interest-free loans to women self-help groups.", "Interest-free loan up to Rs 1 lakh."),
    ("Gujarat", "Vahli Dikri Yojana", "Women & Child Development", "Girl Child",
     "Female", "All", 0, 18, 200000, "All",
     "Financial assistance scheme for the girl child's future.", "Rs 1.1 lakh paid in installments up to age 18."),
    ("Gujarat", "Mukhyamantri Yuva Swavalamban Yojana", "Education", "Education",
     "All", "All", 17, 30, 600000, "Student",
     "Tuition fee assistance for higher education.", "Tuition fee assistance up to Rs 50,000/year."),

    ("Tamil Nadu", "Kalaignar Magalir Urimai Thogai", "Social Welfare", "Welfare",
     "Female", "All", 21, 100, 250000, "Woman-headed household",
     "Monthly income support to women heads of families.", "Rs 1,000/month direct benefit transfer."),
    ("Tamil Nadu", "Moovalur Ramamirtham Ammaiyar Higher Education Scheme", "Social Welfare",
     "Education", "Female", "All", 17, 30, 250000, "Student",
     "Financial assistance for girl students pursuing higher education.", "Rs 1,000-5,000/month stipend."),
    ("Tamil Nadu", "Pudhumai Penn Scheme", "School Education", "Education", "Female",
     "All", 17, 22, 250000, "Student",
     "Monthly assistance for girls from government schools joining higher education.",
     "Rs 1,000/month for the duration of the course."),

    ("Uttar Pradesh", "Kanya Sumangala Yojana", "Women & Child Development",
     "Girl Child", "Female", "All", 0, 21, 300000, "All",
     "Multi-stage financial assistance for the girl child from birth to graduation.",
     "Total Rs 25,000 in 6 installments."),
    ("Uttar Pradesh", "UP Vidhwa Pension Yojana", "Social Welfare", "Pension",
     "Female", "All", 18, 100, 200000, "Woman-headed household",
     "Pension for widows from economically weaker families.", "Rs 1,000/month pension."),
    ("Uttar Pradesh", "Mukhyamantri Yuva Swarozgar Yojana", "MSME", "Self-Employment",
     "All", "All", 18, 40, -1, "Self-employed",
     "Subsidized loans to unemployed youth for setting up enterprises.",
     "Loans up to Rs 25 lakh (services) / Rs 10 lakh (manufacturing) with subsidy."),

    ("West Bengal", "Kanyashree Prakalpa", "Women & Child Development", "Girl Child",
     "Female", "All", 13, 19, 120000, "Student",
     "Conditional cash transfer to keep girls in school and delay marriage.",
     "Annual scholarship Rs 1,000 + one-time grant Rs 25,000."),
    ("West Bengal", "Lakshmir Bhandar", "Women & Child Development", "Welfare",
     "Female", "All", 25, 60, 100000, "Woman-headed household",
     "Monthly financial assistance to women heads of households.",
     "Rs 1,000-1,200/month direct benefit transfer."),
    ("West Bengal", "Sikshashree Scheme", "Backward Classes Welfare", "Education",
     "All", "SC", 6, 18, 250000, "Student",
     "Financial assistance for SC students in classes 5-8.", "Annual scholarship of Rs 800."),

    ("Rajasthan", "Mukhyamantri Chiranjeevi Swasthya Bima Yojana", "Health",
     "Health", "All", "All", 0, 100, -1, "All",
     "Cashless health insurance for all state families.", "Health cover up to Rs 25 lakh/family/year."),
    ("Rajasthan", "Kalibai Bhil Medhavi Chatra Scooty Yojana", "Higher Education",
     "Education", "Female", "All", 16, 24, 800000, "Student",
     "Scooty for meritorious girl students in government colleges.",
     "Free electric scooty or Rs 30,000 cash equivalent."),
    ("Rajasthan", "Mukhyamantri Yuva Sambal Yojana", "Skill & Employment", "Employment",
     "All", "All", 18, 35, 300000, "Unemployed",
     "Unemployment allowance for educated unemployed youth.", "Rs 3,000-4,500/month allowance."),

    ("Madhya Pradesh", "Mukhyamantri Ladli Behna Yojana", "Women & Child Development",
     "Welfare", "Female", "All", 21, 60, 250000, "Woman-headed household",
     "Monthly financial assistance to married women.", "Rs 1,250/month direct benefit transfer."),
    ("Madhya Pradesh", "Ladli Laxmi Yojana", "Women & Child Development", "Girl Child",
     "Female", "All", 0, 21, 1200000, "All",
     "Long-term savings and education scheme for the girl child.",
     "Total benefit of Rs 1.43 lakh by age 21."),
    ("Madhya Pradesh", "Mukhyamantri Medhavi Vidyarthi Yojana", "Higher Education",
     "Education", "All", "All", 17, 30, 600000, "Student",
     "Tuition fee reimbursement for meritorious students in professional courses.",
     "Full tuition fee up to Rs 1.5 lakh/year."),

    ("Bihar", "Mukhyamantri Kanya Utthan Yojana", "Education", "Girl Child",
     "Female", "All", 0, 25, 300000, "Student",
     "Cash incentives for girls from birth through graduation.",
     "Total up to Rs 54,100 across stages including Rs 50,000 on graduation."),
    ("Bihar", "Mukhyamantri Vidyarthi Cycle Yojana", "Education", "Education",
     "All", "All", 13, 18, 250000, "Student",
     "Bicycle assistance for students in class 9 to improve school access.",
     "Rs 3,000 cash assistance to buy a bicycle."),
    ("Bihar", "Bihar Student Credit Card Scheme", "Education", "Education",
     "All", "All", 17, 30, -1, "Student",
     "Collateral-free education loan for higher studies.", "Loan up to Rs 4 lakh at 4% interest."),

    ("Punjab", "Mukh Mantri Punjab Maa Diya Dhiyan Satikar Yojana", "Social Justice",
     "Welfare", "Female", "All", 18, 100, 200000, "Woman-headed household",
     "Monthly financial assistance to eligible women, higher for Dalit women.",
     "Rs 1,000-1,500/month direct benefit transfer."),
    ("Punjab", "Shagun Scheme", "Social Justice & Empowerment", "Welfare", "Female",
     "SC", 18, 45, 150000, "All",
     "Financial assistance for marriage of daughters of SC/BPL families.",
     "Rs 51,000 one-time grant."),
    ("Punjab", "Punjab Ashirwad Scheme", "Social Justice & Empowerment", "Girl Child",
     "Female", "All", 0, 21, 100000, "All",
     "Savings-linked scheme supporting girl children of poor families.",
     "Fixed deposit maturing to approx Rs 51,000 at age 21."),

    ("Haryana", "Mukhyamantri Parivar Samman Nidhi", "Social Justice & Empowerment",
     "Welfare", "All", "All", 18, 100, 180000, "All",
     "Income support scheme for families below the income threshold.",
     "Financial assistance topping family income to Rs 1 lakh/year."),
    ("Haryana", "Dayalu Yojana", "Social Justice & Empowerment", "Welfare", "All",
     "All", 0, 100, 180000, "All",
     "Financial assistance to families on death of the earning member.",
     "One-time grant of Rs 2-5 lakh."),
    ("Haryana", "Ladli Yojana Haryana", "Women & Child Development", "Girl Child",
     "Female", "All", 0, 18, 200000, "All",
     "Savings scheme for families with girl children.", "Rs 5,000-6,000/year deposited annually."),

    ("Delhi", "Delhi Mukhyamantri Mahila Samman Yojana", "Women & Child Development",
     "Welfare", "Female", "All", 18, 100, 300000, "Woman-headed household",
     "Monthly financial assistance to adult women residents.", "Rs 1,000-2,100/month direct benefit transfer."),
    ("Delhi", "Delhi Ladli Scheme", "Women & Child Development", "Girl Child",
     "Female", "All", 0, 18, 100000, "All",
     "Savings-linked scheme for the girl child's education.", "Total up to Rs 1 lakh disbursed in stages."),
    ("Delhi", "Atal Canteen Scheme", "DUSIB", "Food Security", "All", "All", 0, 100,
     -1, "All", "Subsidized meals through government-run canteens.", "Meals at highly subsidized rates."),

    ("Kerala", "Aardram Mission", "Health", "Health", "All", "All", 0, 100, 100000,
     "All", "Strengthening public healthcare access and family health centres.",
     "Free OP/IP treatment at upgraded family health centres."),
    ("Kerala", "Snehapoorvam Scheme", "Social Justice", "Welfare", "All", "All", 0,
     18, 100000, "All", "Financial assistance for orphaned/destitute children.",
     "Rs 300-500/month assistance."),
    ("Kerala", "Kerala Karunya Health Scheme", "Health", "Health", "All", "All", 0,
     100, 300000, "All", "Financial assistance for treatment of critical illnesses.",
     "Assistance up to Rs 3 lakh for critical treatment."),

    ("Telangana", "Rythu Bandhu", "Agriculture", "Agriculture", "All", "All", 18,
     100, -1, "Farmer", "Investment support scheme for farmers per crop season.",
     "Rs 10,000/acre/year in two installments."),
    ("Telangana", "KCR Kit Scheme", "Health", "Maternity", "Female", "All", 18, 45,
     -1, "All", "Financial assistance and nutrition kit for pregnant/lactating mothers.",
     "Rs 12,000-13,000 cash + nutrition kit."),
    ("Telangana", "Telangana Aasara Pension", "Social Welfare", "Pension", "All",
     "All", 57, 100, 200000, "Senior Citizen",
     "Social security pension for elderly, disabled, and widows.", "Rs 2,016-3,016/month pension."),

    ("Andhra Pradesh", "YSR Cheyutha", "Women & Child Development", "Welfare",
     "Female", "SC", 45, 60, 150000, "Woman-headed household",
     "Financial assistance to SC/ST/BC/minority women for self-employment.",
     "Rs 18,750/year for 4 years."),
    ("Andhra Pradesh", "Amma Vodi", "School Education", "Education", "Female",
     "All", 25, 100, 100000, "Student",
     "Financial assistance to mothers/guardians to send children to school.",
     "Rs 15,000/year per child."),
    ("Andhra Pradesh", "YSR Pension Kanuka", "Social Welfare", "Pension", "All",
     "All", 60, 100, 150000, "Senior Citizen",
     "Enhanced social security pension for elderly and vulnerable groups.",
     "Rs 3,000/month pension."),

    ("Odisha", "Biju Krushak Kalyan Yojana", "Agriculture", "Agriculture", "All",
     "All", 18, 100, 100000, "Farmer",
     "Health and financial protection scheme for small/marginal farmers.",
     "Health cover + Rs 2,000/season income support."),
    ("Odisha", "Madhu Babu Pension Yojana", "Social Security & Empowerment of PWD",
     "Pension", "All", "All", 58, 100, 100000, "Senior Citizen",
     "Pension for elderly, widows and persons with disabilities.", "Rs 500-700/month pension."),
    ("Odisha", "KALIA Scheme", "Agriculture", "Agriculture", "All", "All", 18, 100,
     -1, "Farmer", "Financial assistance to cultivators and landless agricultural households.",
     "Rs 10,000/year support for farm families."),

    ("Punjab", "Sarbat Sehat Bima Yojana", "Health & Family Welfare", "Health",
     "All", "All", 0, 100, 200000, "All",
     "Cashless health insurance for poor and vulnerable families.",
     "Health cover up to Rs 5 lakh/family/year."),

    ("Assam", "Orunodoi Scheme", "Social Welfare", "Welfare", "Female", "All", 18,
     100, 200000, "Woman-headed household",
     "Direct cash transfer to economically weaker households, via women beneficiaries.",
     "Rs 1,250/month direct benefit transfer."),
    ("Assam", "Assam Nijut Moina Scholarship", "Education", "Education", "Female",
     "All", 13, 24, 250000, "Student",
     "Scholarship for girl students from class 9 to postgraduate level.",
     "Rs 1,000-2,500/month based on class."),
    ("Assam", "Chief Minister's Samagra Gramya Unnayan Yojana", "Rural Development",
     "Rural Development", "All", "All", 18, 100, 150000, "Farmer",
     "Comprehensive rural development and livelihood support scheme.",
     "Grants for agriculture, livestock and micro-enterprise."),

    ("Chandigarh", "Chandigarh Ladli Scheme", "Social Welfare",
     "Girl Child", "Female", "All", 0, 21, 150000, "All",
     "Savings and incentive scheme for the girl child.",
     "Cash incentives at school milestones up to age 21."),

    ("Jharkhand", "Mukhyamantri Sukanya Yojana", "Women & Child Development",
     "Girl Child", "Female", "All", 0, 18, 150000, "All",
     "Financial assistance for education of girl children.",
     "Rs 40,000 disbursed across schooling milestones."),
    ("Jharkhand", "Mukhyamantri Rojgar Srijan Yojana", "Industries", "Self-Employment",
     "All", "All", 18, 45, -1, "Self-employed",
     "Subsidized loans for setting up small enterprises.", "Subsidy up to 40% of project cost."),
    ("Jharkhand", "Abua Awas Yojana", "Rural Development", "Housing", "All", "All",
     18, 100, 100000, "All", "State housing scheme for households without pucca homes.",
     "Financial assistance of Rs 2 lakh to build a house."),

    ("Chhattisgarh", "Mahtari Vandan Yojana", "Women & Child Development", "Welfare",
     "Female", "All", 21, 100, 250000, "Woman-headed household",
     "Monthly financial assistance to married women.", "Rs 1,000/month direct benefit transfer."),
    ("Chhattisgarh", "Godhan Nyay Yojana", "Rural Development", "Agriculture",
     "All", "All", 18, 100, -1, "Farmer",
     "Cow dung procurement scheme supporting rural livelihoods.",
     "Rs 2/kg for cow dung purchased from farmers/cattle-rearers."),
    ("Chhattisgarh", "Chhattisgarh Medhavi Chhatra Yojana", "Higher Education",
     "Education", "All", "All", 17, 30, 250000, "Student",
     "Fee waiver for meritorious economically weak students.", "Full tuition fee waiver."),

    ("Punjab (Uttarakhand)", "placeholder", "x", "x", "All", "All", 0, 0, 0, "All", "x", "x"),

    ("Uttarakhand", "Mukhyamantri Ghasyari Kalyan Yojana", "Agriculture", "Agriculture",
     "Female", "All", 18, 100, 150000, "Farmer",
     "Support for women farmers/livestock-rearers to ease fodder collection burden.",
     "Rs 3,000-4,000/year support."),
    ("Uttarakhand", "Uttarakhand Nandadevi Kanya Yojana", "Women & Child Development",
     "Girl Child", "Female", "All", 0, 18, 150000, "All",
     "One-time grant on the birth of a girl child in the family.",
     "Rs 50,000 fixed deposit maturing at age 18."),
    ("Uttarakhand", "Uttarakhand Vridha Pension Yojana", "Social Welfare", "Pension",
     "All", "All", 60, 100, 100000, "Senior Citizen",
     "Old age pension for economically weaker senior citizens.", "Rs 1,200-1,400/month pension."),

    ("Himachal Pradesh", "Mukhyamantri Sukh Ashraya Yojana", "Social Justice",
     "Welfare", "All", "All", 0, 27, 100000, "All",
     "Support for orphaned and destitute children until self-sufficiency.",
     "Full education, health and monthly stipend support."),
    ("Himachal Pradesh", "Himachal Pradesh Vidhwa Punarvivah Yojana", "Social Justice",
     "Welfare", "Female", "All", 18, 100, 100000, "Woman-headed household",
     "Incentive for remarriage of widows.", "One-time grant of Rs 50,000."),
    ("Himachal Pradesh", "Himcare Yojana", "Health & Family Welfare", "Health",
     "All", "All", 0, 100, 300000, "All",
     "Health insurance for families not covered under Ayushman Bharat.",
     "Health cover up to Rs 5 lakh/family/year."),

    ("Goa", "Ladli Laxmi Yojana Goa", "Women & Child Development", "Girl Child",
     "Female", "All", 0, 18, 800000, "All",
     "Financial assistance scheme for the girl child.", "Rs 1 lakh maturity bond at age 18."),
    ("Goa", "Griha Aadhar Scheme", "Women & Child Development", "Welfare", "Female",
     "All", 18, 100, 300000, "Woman-headed household",
     "Financial assistance to housewives to strengthen family finances.",
     "Rs 1,500/month direct benefit transfer."),
    ("Goa", "Deen Dayal Swasthya Seva Yojana", "Health", "Health", "All", "All", 0,
     100, 400000, "All", "Cashless health insurance for Goa residents.",
     "Health cover up to Rs 4 lakh/family/year."),

    ("Manipur", "Chief Minister's Hakshelgi Tengbang", "Health", "Health", "All",
     "All", 0, 100, 400000, "All",
     "Health insurance scheme for state residents.", "Health cover up to Rs 2 lakh/family/year."),
    ("Manipur", "Chief Minister Elite Athletes Scheme", "Youth Affairs & Sports",
     "Education", "All", "All", 14, 30, -1, "Student",
     "Financial support and training for elite athletes.", "Monthly stipend + training support."),

    ("Meghalaya", "Chief Minister's Elderly Support Scheme", "Social Welfare",
     "Pension", "All", "All", 60, 100, 100000, "Senior Citizen",
     "Monthly pension for elderly citizens.", "Rs 300-500/month pension."),
    ("Meghalaya", "Meghalaya Livelihoods and Access to Markets", "Rural Development",
     "Self-Employment", "All", "All", 18, 60, 150000, "Self-employed",
     "Support for farmer producer groups and rural entrepreneurs.",
     "Grants and market linkage support."),

    ("Tripura", "Chief Minister Jubak Jubati Karmasangsthan Yojana", "Labour",
     "Employment", "All", "All", 18, 40, 150000, "Unemployed",
     "Self-employment loans for unemployed youth.", "Subsidized loan up to Rs 2 lakh."),
    ("Tripura", "Tripura Swanirbhar Scheme", "Rural Development", "Self-Employment",
     "All", "All", 18, 100, 150000, "Self-employed",
     "Support for self-help groups and rural micro-enterprises.",
     "Revolving fund and skill training support."),

    ("Mizoram", "New Land Use Policy (NLUP)", "Agriculture", "Agriculture", "All",
     "All", 18, 100, 150000, "Farmer",
     "Support to shift from shifting cultivation to sustainable farming.",
     "Financial and input support for approved farm projects."),
    ("Mizoram", "Mizoram Chief Minister Rural Housing Scheme", "Rural Development",
     "Housing", "All", "All", 18, 100, 100000, "All",
     "Housing assistance for rural poor families.", "Financial assistance to build a pucca house."),

    ("Nagaland", "Chief Minister's Health Insurance Scheme", "Health", "Health",
     "All", "All", 0, 100, 300000, "All",
     "Health insurance cover for state residents.", "Health cover up to Rs 5 lakh/family/year."),
    ("Nagaland", "Nagaland Rural Livelihood Mission", "Rural Development",
     "Self-Employment", "All", "All", 18, 100, 150000, "Self-employed",
     "Self-help-group based livelihood promotion.", "Revolving fund + bank linkage support."),

    ("Sikkim", "Sikkim Chief Minister's Comprehensive Annual and Family Health Scheme",
     "Health", "Health", "All", "All", 0, 100, -1, "All",
     "Universal health checkup and insurance scheme for all residents.",
     "Free annual health checkup + health insurance."),
    ("Sikkim", "Sikkim Girl Child Protection Scheme", "Social Justice", "Girl Child",
     "Female", "All", 0, 18, 200000, "All",
     "Savings-linked scheme for the girl child.", "Fixed deposit maturing at age 18."),

    ("Arunachal Pradesh", "Chief Minister's Adarsh Gram Yojana", "Rural Development",
     "Rural Development", "All", "All", 18, 100, 100000, "All",
     "Model village development scheme for infrastructure and livelihood.",
     "Infrastructure grants and livelihood support per village."),
    ("Arunachal Pradesh", "Arunachal Pradesh Chief Minister's Nyokum Yollo Scholarship",
     "Education", "Education", "All", "ST", 13, 24, 200000, "Student",
     "Scholarship support for tribal students.", "Annual scholarship amount for tuition/hostel fees."),

    ("Punjab (UT)", "placeholder2", "x", "x", "All", "All", 0, 0, 0, "All", "x", "x"),
]

for row in STATE_SCHEMES:
    state, name, dept, category, gender, caste, min_age, max_age, max_income, occ, desc, benefit = row
    if name in ("placeholder", "placeholder2"):
        continue
    add(name, "State", state, dept, category, gender, caste, min_age, max_age,
        max_income, occ, desc, benefit, "https://services.india.gov.in")

# ---------------------------------------------------------------
# Union Territories
# ---------------------------------------------------------------
UT_SCHEMES = [
    ("Jammu and Kashmir", "J&K Reshi Aabadkari Scheme", "Revenue", "Housing",
     "All", "All", 18, 100, 100000, "All",
     "Land/housing assistance to landless and homeless families.",
     "Land allotment/financial assistance for house construction."),
    ("Jammu and Kashmir", "Sher-e-Kashmir Employment & Welfare Programme for Youth",
     "Skill Development & Entrepreneurship", "Self-Employment", "All", "All", 18, 40,
     -1, "Unemployed", "Self-employment support scheme for educated unemployed youth.",
     "Subsidized loan + margin money support."),
    ("Ladakh", "Ladakh Chief Executive Councillor's Solar Scheme", "Rural Development",
     "Welfare", "All", "All", 18, 100, 150000, "All",
     "Solar electrification support for remote households.",
     "Subsidized solar home lighting units."),
    ("Puducherry", "Puducherry Kalvi Ulavan Thittam", "Agriculture", "Agriculture",
     "All", "All", 18, 100, 150000, "Farmer",
     "Support for farmer welfare and agricultural inputs.", "Input subsidy and equipment support."),
    ("Chandigarh", "Chandigarh Social Security Pension Scheme", "Social Welfare",
     "Pension", "All", "All", 60, 100, 100000, "Senior Citizen",
     "Old age/widow/disability pension for UT residents.", "Rs 1,500-2,000/month pension."),
    ("Andaman and Nicobar Islands", "A&N Fisherman Welfare Scheme", "Fisheries",
     "Welfare", "All", "All", 18, 100, 150000, "All",
     "Support for fishing community livelihoods.", "Boat/gear subsidy and insurance support."),
    ("Dadra and Nagar Haveli and Daman and Diu", "DNHDD Beti Hai Anmol Yojana",
     "Women & Child Development", "Girl Child", "Female", "All", 0, 18, 150000,
     "All", "Savings scheme for the girl child.", "Cash incentives at schooling milestones."),
    ("Lakshadweep", "Lakshadweep Fisherman Savings-cum-Relief Scheme", "Fisheries",
     "Welfare", "All", "All", 18, 60, 150000, "All",
     "Savings-linked relief scheme for fishermen during lean season.",
     "Matching government contribution to fisherman savings."),
]
for state, name, dept, category, gender, caste, min_age, max_age, max_income, occ, desc, benefit in UT_SCHEMES:
    add(name, "State", state, dept, category, gender, caste, min_age, max_age,
        max_income, occ, desc, benefit, "https://services.india.gov.in")

# ---------------------------------------------------------------
# Write CSV
# ---------------------------------------------------------------
HEADER = ["scheme_id", "scheme_name", "level", "state", "department", "category",
          "gender", "caste_category", "min_age", "max_age", "max_income",
          "occupation", "description", "benefits", "official_link"]

with open("schemes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    w.writerows(ROWS)

states_covered = sorted(set(r[3] for r in ROWS if r[2] == "State"))
print(f"Total schemes: {len(ROWS)}")
print(f"States/UTs covered: {len(states_covered)}")
for s in states_covered:
    print(" -", s)
