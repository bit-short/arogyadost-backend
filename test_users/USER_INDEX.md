# Test Users Index

## User Directory Format: `user_XXX_YYZ`
- XXX = User number (001-020)
- YY = Age 
- Z = Gender (f/m)

## Complete User List

### Users with Medical Data (OCR/Comprehensive)
- **user_001_29f** - 29-year-old female (comprehensive medical data from OCR)
- **user_003_31m** - 31-year-old male (medical data from OCR)
- **user_004_31m** - 31-year-old male (medical data from OCR)
- **user_007_27f** - 27-year-old female (basic health package)
- **user_009_26f** - 26-year-old female (women's health panel)
- **user_011_34f** - 34-year-old female (comprehensive health package)
- **user_013_24f** - 24-year-old female (basic panel)
- **user_015_23f** - 23-year-old female (young adult panel)
- **user_018_39m** - 39-year-old male (executive health package)

### Users with Minimal Data
- **user_002_29m** - 29-year-old male (empty documents)
- **user_005_55f** - 55-year-old female (empty documents)
- **user_006_65m** - 65-year-old male (empty documents)
- **user_008_33m** - 33-year-old male (empty documents)
- **user_010_30m** - 30-year-old male (empty documents)
- **user_012_36m** - 36-year-old male (empty documents)
- **user_014_37m** - 37-year-old male (empty documents)
- **user_016_38m** - 38-year-old male (empty documents)
- **user_017_22f** - 22-year-old female (empty documents)
- **user_019_21f** - 21-year-old female (empty documents)
- **user_020_40m** - 40-year-old male (empty documents)

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
