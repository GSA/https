
#########################################################
#
# Just scratch space, this won't execute or import properly.
#
#########################################################

name = "Pre-BOD (all executive)"
compliance_stats(name, pre_bod[-1], utils.executive_only)

name = "Most recent (all executive)"
compliance_stats(name, post_bod[-1], utils.executive_only)

name = "Most recent (all legislative)"
compliance_stats(name, post_bod[-1], utils.legislative_only)

name = "Most recent (all judicial)"
compliance_stats(name, post_bod[-1], utils.judicial_only)

name = "Most recent (CFO Act only)"
compliance_stats(name, post_bod[-1], utils.cfo_act_only)

name = "Most recent (CFO Act only, minus DoD)"
compliance_stats(name, post_bod[-1], utils.cfo_act_only_sans_dod)

name = "Most recent (DoD only)"
compliance_stats(name, post_bod[-1], utils.for_agencies(["Department of Defense"]))

name = "Most recent (non-CFO Act)"
compliance_stats(name, post_bod[-1], utils.executive_non_cfo_act)


# All executive hostnames pre-BOD.
compliance_csv(pre_bod, "pre",
  utils.executive_only,
  "cache/pre-bod-executive.csv"
)
# All executive hostnames post-BOD.
compliance_csv(post_bod, "post",
  utils.executive_only,
  "cache/post-bod-executive.csv"
)

# CFO Act
compliance_csv(pre_bod, "pre",
  utils.cfo_act_only,
  "cache/pre-bod-cfo.csv"
)
compliance_csv(post_bod, "post",
  utils.cfo_act_only,
  "cache/post-bod-cfo.csv"
)

# Non-CFO Act
compliance_csv(pre_bod, "pre",
  utils.executive_non_cfo_act,
  "cache/pre-bod-non-cfo.csv"
)
compliance_csv(post_bod, "post",
  utils.executive_non_cfo_act,
  "cache/post-bod-non-cfo.csv"
)

# CFO Act (minus DoD)
compliance_csv(pre_bod, "pre",
  utils.cfo_act_only_sans_dod,
  "cache/pre-bod-cfo-no-dod.csv"
)
compliance_csv(post_bod, "post",
  utils.cfo_act_only_sans_dod,
  "cache/post-bod-cfo-no-dod.csv"
)

# DoD only
compliance_csv(pre_bod, "pre",
  utils.for_agencies(["Department of Defense"]),
  "cache/pre-bod-dod.csv"
)
compliance_csv(post_bod, "post",
  utils.for_agencies(["Department of Defense"]),
  "cache/post-bod-dod.csv"
)


cfo_act_groups = [
  "U.S. Department of Agriculture",
  "Department of Commerce",
  "Department of Defense",
  "Department of Education",
  "Department of Energy",
  "Department of Health and Human Services",
  "Department of Homeland Security",
  "Department of Housing and Urban Development",
  "Department of the Interior",
  [
    "Department of Justice",
    "Terrorist Screening Center", # (DOJ/FBI) as seen in .gov data
  ],
  "Department of Labor",
  [
    "Department of State",
    "Department of State, Office of Inspector General", # seen in .gov data
  ],
  "Department of Transportation",
  "Department of the Treasury",
  "Department of Veterans Affairs",
  "Environmental Protection Agency",
  "National Aeronautics and Space Administration",
  "U.S. Agency for International Development",
  "General Services Administration",
  "National Science Foundation",
  "Nuclear Regulatory Commission",
  "Office of Personnel Management",
  "Small Business Administration",
  "Social Security Administration"
]
