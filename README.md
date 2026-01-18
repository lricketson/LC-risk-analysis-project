'Fully Paid': 7189
'Charged Off': 1713
'Current': 1024
'Late (31-120 days)': 58
'In Grace Period': 12
'Late (16-30 days)': 4

Only kept Fully Paid and Charged Off loans

term: ie 60 months, change to just 60 !
grade and subgrade: collapse to grade only, then encode numerically on a scale of 1 to 7
purpose: one-hot encode
verification_status: 0 for not, 1 for verified, 2 for source verified
home_ownership: encode categorical
earliest_cr_line: convert to acc age in years
