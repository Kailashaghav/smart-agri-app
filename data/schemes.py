# ==============================================================
# Government Schemes Data
# ==============================================================

GOVT_SCHEMES = [
    {
        "name": "PM-KISAN",
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "emoji": "💰",
        "benefit": "₹6,000/year in 3 equal instalments of ₹2,000 directly to farmer's bank account.",
        "eligibility": "All small and marginal farmers owning cultivable land. Excludes income-tax payers, institutional landholders.",
        "how_to_apply": "1. Visit pmkisan.gov.in\n2. Click 'Farmer Corner → New Farmer Registration'\n3. Enter Aadhaar number and land details\n4. Verify via OTP\n5. Approval by local tehsildar/patwari",
        "documents": "Aadhaar Card, Land Records (Khasra/Khatauni), Bank Passbook, Mobile Number",
        "helpline": "PM-KISAN Helpline: 155261 / 011-24300606",
        "website": "https://pmkisan.gov.in",
        "color": [0.1, 0.6, 0.3, 1],
    },
    {
        "name": "PMFBY",
        "full_name": "Pradhan Mantri Fasal Bima Yojana",
        "emoji": "🛡️",
        "benefit": "Crop insurance coverage for losses due to natural calamities, pests, and diseases. Farmers pay only 1.5–2% premium for Kharif, 2% for Rabi crops.",
        "eligibility": "All farmers growing notified crops in notified areas. Both loanee and non-loanee farmers eligible.",
        "how_to_apply": "1. Apply at nearest bank branch or CSC\n2. Or apply online at pmfby.gov.in\n3. Submit before cut-off date (usually 2 weeks before sowing)\n4. Required: Aadhaar, land records, bank account, sowing certificate",
        "documents": "Aadhaar, Land Records, Bank Account, Sowing Certificate, Mobile Number",
        "helpline": "PMFBY Helpline: 1800-180-1551 (Toll-free)",
        "website": "https://pmfby.gov.in",
        "color": [0.1, 0.4, 0.8, 1],
    },
    {
        "name": "Kisan Credit Card",
        "full_name": "Kisan Credit Card (KCC) Scheme",
        "emoji": "💳",
        "benefit": "Revolving credit up to ₹3 lakh at 4% interest rate (after 2% interest subvention + 3% prompt repayment incentive). Covers crop cultivation, post-harvest, allied activities.",
        "eligibility": "All farmers — individual/joint borrowers, tenant farmers, oral lessees, share croppers, SHGs.",
        "how_to_apply": "1. Visit nearest bank (SBI, PNB, Cooperative banks, RRBs)\n2. Fill KCC application form\n3. Submit land documents, Aadhaar, photos\n4. Bank will process within 2 weeks",
        "documents": "Application Form, 2 Passport Photos, Aadhaar, Land Records, Bank Account",
        "helpline": "Agricultural Dept Helpline: 1800-180-1551",
        "website": "https://www.nabard.org/content1.aspx?id=572",
        "color": [0.7, 0.3, 0.1, 1],
    },
    {
        "name": "Soil Health Card",
        "full_name": "Soil Health Card Scheme",
        "emoji": "🌍",
        "benefit": "Free soil testing and personalised nutrient recommendations. Helps reduce fertiliser costs by 10–25% through balanced application.",
        "eligibility": "All farmers across India. Free of cost.",
        "how_to_apply": "1. Contact local Krishi Vigyan Kendra (KVK) or Agriculture Department\n2. Or visit soilhealth.dac.gov.in\n3. Soil sample collected every 2 years\n4. Card delivered with crop-wise fertiliser recommendation",
        "documents": "Land ownership proof, Aadhaar Card",
        "helpline": "soilhealth.dac.gov.in | State Agriculture Dept",
        "website": "https://soilhealth.dac.gov.in",
        "color": [0.5, 0.35, 0.1, 1],
    },
    {
        "name": "e-NAM",
        "full_name": "National Agriculture Market (e-NAM)",
        "emoji": "🏪",
        "benefit": "Online trading platform for agricultural commodities. Farmers get better price discovery and reduced dependence on middlemen.",
        "eligibility": "All farmers with registered produce. Available in 1,000+ mandis across 18 states.",
        "how_to_apply": "1. Register at enam.gov.in or visit nearest APMC mandi\n2. Complete KYC with Aadhaar and bank details\n3. Upload quality test report of produce\n4. Auction your produce online",
        "documents": "Aadhaar, Bank Account, Mobile Number, Produce Quality Report",
        "helpline": "e-NAM Helpline: 1800-270-0224",
        "website": "https://enam.gov.in",
        "color": [0.2, 0.5, 0.7, 1],
    },
    {
        "name": "NMSA",
        "full_name": "National Mission for Sustainable Agriculture",
        "emoji": "♻️",
        "benefit": "Subsidies for drip/sprinkler irrigation, organic farming inputs, soil health management, watershed development. Up to 50–55% subsidy on micro-irrigation.",
        "eligibility": "All farmers. Small/marginal farmers get higher subsidy (55%).",
        "how_to_apply": "1. Contact District Agriculture Officer\n2. Apply through state agriculture department portal\n3. Inspection of land and approval\n4. Subsidy credited after installation",
        "documents": "Aadhaar, Land Records, Bank Account, Quotation from approved supplier",
        "helpline": "State Agriculture Department",
        "website": "https://nmsa.dac.gov.in",
        "color": [0.1, 0.7, 0.4, 1],
    },
    {
        "name": "PM Kusum",
        "full_name": "PM Kisan Urja Suraksha evam Utthan Mahabhiyan",
        "emoji": "☀️",
        "benefit": "Solar pump subsidies (up to 90% for small/marginal farmers). Solarise existing grid-connected pumps. Install solar power plants on barren land.",
        "eligibility": "All farmers. Priority to small/marginal farmers.",
        "how_to_apply": "1. Apply online at mnre.gov.in or state nodal agency\n2. Or visit District Renewable Energy Office\n3. Select component (A/B/C)\n4. Pay farmer's share (10%) after approval",
        "documents": "Aadhaar, Land Records, Bank Account, Existing pump details",
        "helpline": "MNRE Helpline: 011-2436-0707",
        "website": "https://mnre.gov.in/solar/schemes",
        "color": [0.9, 0.6, 0.1, 1],
    },
    {
        "name": "Paramparagat Krishi",
        "full_name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "emoji": "🌿",
        "benefit": "₹50,000/ha over 3 years for organic farming. Includes ₹31,000 for organic inputs, ₹8,800 for value addition, ₹3,000 for distribution.",
        "eligibility": "Farmer groups of 50 members covering 50 acres. Focus on organic farming conversion.",
        "how_to_apply": "1. Form a cluster of 50 farmers\n2. Apply through State Agriculture Department\n3. Submit organic farming plan\n4. Third-party certification after 3 years",
        "documents": "Group registration, Land Records, Bank Accounts of all members",
        "helpline": "pkvy.dac.gov.in | State Agriculture Dept",
        "website": "https://pkvy.dac.gov.in",
        "color": [0.2, 0.65, 0.2, 1],
    },
]


# ==============================================================
# Crop Recommendation Engine
# ==============================================================

CROP_RECOMMENDATIONS = {
    # Format: (soil_type, season) -> list of crop recommendations
    ("Black/Cotton", "Kharif"): {
        "crops": ["Cotton", "Soybean", "Jowar (Sorghum)", "Tur (Pigeon Pea)"],
        "reason": "Black soil (Vertisol) retains moisture well, ideal for cotton and soybean in Kharif season.",
        "tips": "Cotton performs best in black soil with good drainage. Apply 120:60:60 kg NPK/ha for cotton.",
        "water_need": "Medium",
        "investment": "Medium–High",
    },
    ("Black/Cotton", "Rabi"): {
        "crops": ["Wheat", "Chickpea (Gram)", "Safflower", "Linseed"],
        "reason": "Black soil retains Kharif moisture for Rabi crops without irrigation.",
        "tips": "Chickpea is excellent for nitrogen fixation. Ideal for dryland Rabi cropping.",
        "water_need": "Low",
        "investment": "Low–Medium",
    },
    ("Black/Cotton", "Summer/Zaid"): {
        "crops": ["Sunflower", "Groundnut", "Moong (Green Gram)", "Watermelon"],
        "reason": "Short-duration crops that can utilise residual moisture in black soil.",
        "tips": "Sunflower is drought-tolerant and gives good yield in summer.",
        "water_need": "Low–Medium",
        "investment": "Low",
    },
    ("Red/Laterite", "Kharif"): {
        "crops": ["Groundnut", "Finger Millet (Ragi)", "Maize", "Cowpea"],
        "reason": "Red soils are well-drained, slightly acidic — ideal for groundnut and millets.",
        "tips": "Apply lime if pH < 6. Groundnut needs gypsum application at flowering stage.",
        "water_need": "Medium",
        "investment": "Low–Medium",
    },
    ("Red/Laterite", "Rabi"): {
        "crops": ["Horsegram", "Field Bean", "Mustard", "Potato"],
        "reason": "Red soils drain quickly; choose drought-tolerant Rabi crops.",
        "tips": "Add organic matter (FYM) to improve red soil water-holding capacity.",
        "water_need": "Low",
        "investment": "Low",
    },
    ("Red/Laterite", "Summer/Zaid"): {
        "crops": ["Sesame", "Cowpea", "Moong Bean", "Bitter Gourd"],
        "reason": "Short-duration crops that tolerate heat and need less water.",
        "tips": "Sesame is highly profitable in summer on red soils with minimal inputs.",
        "water_need": "Low",
        "investment": "Low",
    },
    ("Alluvial", "Kharif"): {
        "crops": ["Rice", "Sugarcane", "Jute", "Maize", "Vegetables"],
        "reason": "Alluvial soils are highly fertile with good water retention — ideal for rice.",
        "tips": "SRI (System of Rice Intensification) method can increase rice yield by 25–50%.",
        "water_need": "High",
        "investment": "Medium",
    },
    ("Alluvial", "Rabi"): {
        "crops": ["Wheat", "Mustard", "Potato", "Peas", "Onion"],
        "reason": "Fertile alluvial soils with canal/tubewell irrigation support high-value Rabi crops.",
        "tips": "Wheat + Mustard rotation is classic in Indo-Gangetic plains. Very profitable.",
        "water_need": "Medium",
        "investment": "Medium",
    },
    ("Alluvial", "Summer/Zaid"): {
        "crops": ["Cucumber", "Okra", "Bottle Gourd", "Sweet Corn", "Mung Bean"],
        "reason": "With irrigation, alluvial soils support high-value vegetable crops in summer.",
        "tips": "Vegetable crops give 3x more income per acre than cereal crops.",
        "water_need": "High",
        "investment": "Medium–High",
    },
    ("Sandy/Loam", "Kharif"): {
        "crops": ["Pearl Millet (Bajra)", "Groundnut", "Cluster Bean", "Moong"],
        "reason": "Sandy soils drain fast; drought-tolerant crops perform best.",
        "tips": "Bajra needs very little water and gives good yield even in 300–500mm rainfall areas.",
        "water_need": "Low",
        "investment": "Low",
    },
    ("Sandy/Loam", "Rabi"): {
        "crops": ["Mustard", "Barley", "Gram", "Cumin"],
        "reason": "Sandy loam is ideal for mustard and spice crops in dry Rabi season.",
        "tips": "Cumin is a high-value spice crop — very profitable in Rajasthan/Gujarat sandy soils.",
        "water_need": "Low",
        "investment": "Low",
    },
    ("Sandy/Loam", "Summer/Zaid"): {
        "crops": ["Watermelon", "Muskmelon", "Fodder crops", "Sesame"],
        "reason": "Sandy soil with light irrigation supports melon crops in summer very well.",
        "tips": "Watermelon and muskmelon give excellent returns in summer on sandy soils.",
        "water_need": "Medium",
        "investment": "Low–Medium",
    },
    ("Clay", "Kharif"): {
        "crops": ["Rice", "Jute", "Sugarcane", "Taro"],
        "reason": "Clay soils retain water well — suitable for water-loving crops.",
        "tips": "Improve drainage before planting to avoid waterlogging damage.",
        "water_need": "High",
        "investment": "Medium",
    },
    ("Clay", "Rabi"): {
        "crops": ["Wheat", "Lentil (Masoor)", "Berseem (Fodder)"],
        "reason": "Clay soil retains moisture from Kharif rains for Rabi cultivation.",
        "tips": "Avoid heavy machinery on wet clay to prevent soil compaction.",
        "water_need": "Low–Medium",
        "investment": "Medium",
    },
    ("Clay", "Summer/Zaid"): {
        "crops": ["Moong Bean", "Sunflower", "Okra"],
        "reason": "Short-duration crops on residual clay moisture.",
        "tips": "Sunflower is the best summer crop for clay soils — good oil content.",
        "water_need": "Medium",
        "investment": "Low",
    },
}

SOIL_TYPES = ["Black/Cotton", "Red/Laterite", "Alluvial", "Sandy/Loam", "Clay"]
SEASONS    = ["Kharif", "Rabi", "Summer/Zaid"]


def get_crop_recommendation(soil: str, season: str) -> dict:
    """Return crop recommendation for given soil and season."""
    key = (soil, season)
    return CROP_RECOMMENDATIONS.get(key, {
        "crops": ["Consult your local KVK for personalised recommendations"],
        "reason": "No specific data available for this combination.",
        "tips": "Contact your nearest Krishi Vigyan Kendra for expert advice.",
        "water_need": "Unknown",
        "investment": "Unknown",
    })
