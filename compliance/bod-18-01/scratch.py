
#########################################################
#
# Just scratch space, this won't execute or import properly.
#
#########################################################


name = "Most recent (all executive)"
compliance_stats(name, post_bods[-1], utils.executive_only)





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
