# Test Users Index

## User Directory Format: `user_XXX_YYZ`
- XXX = User number 
- YY = Age 
- Z = Gender (f/m)

## Current Users with Medical Data

### OCR-Extracted Real Data
- **user_001_29f** - 29-year-old female (comprehensive OCR medical data - 18 pages)
- **user_003_31m** - 31-year-old male (OCR medical data)
- **user_004_31m** - 31-year-old male (OCR medical data)

### Generated Medical Data
- **user_007_27f** - 27-year-old female (basic health package)
- **user_009_26f** - 26-year-old female (women's health panel)
- **user_011_34f** - 34-year-old female (comprehensive health package)
- **user_013_24f** - 24-year-old female (basic panel)
- **user_015_23f** - 23-year-old female (young adult panel)
- **user_018_39m** - 39-year-old male (executive health package)

## Quick Commands
```bash
# List all users
ls test_users/user_*/

# Check specific user
cat test_users/user_001_29f/profile.json

# Find users by age range
ls test_users/user_*_2[0-9]*/  # 20-29 years old
ls test_users/user_*_3[0-9]*/  # 30-39 years old

# Find users by gender
ls test_users/user_*f/  # Female users
ls test_users/user_*m/  # Male users
```
