# Logo Files Required

## Missing Logo Files

Please add your MIVA logo files to this directory:

### 1. Light Mode Logo
**Filename**: `miva_logo_light.png`

**Design**:
- Dark or colored logo (visible on white/light backgrounds)
- Works on: #FFFFFF (white) and #F0F2F6 (light gray)

**Specifications**:
- Format: PNG with transparency
- Width: 200-300px
- Height: Proportional
- Max Size: 500KB

### 2. Dark Mode Logo
**Filename**: `miva_logo_dark.png`

**Design**:
- White or very light colored logo (visible on dark backgrounds)
- Works on: #0E1117 (deep black) and #262730 (dark gray)

**Specifications**:
- Format: PNG with transparency
- Width: 200-300px
- Height: Proportional
- Max Size: 500KB

### 3. Optional Fallback Logo
**Filename**: `miva_logo.png`

This is used if the theme-specific logos are not found.

## How to Add Logos

1. Design or export your logo in both light and dark versions
2. Save them with the exact filenames above
3. Place them in this `assets/` directory
4. The dashboard will automatically detect and display them

## Testing Your Logos

After adding the logos:
1. Run the dashboard locally: `streamlit run app.py`
2. Toggle dark mode using the 🌙/☀️ button
3. Verify both logos display correctly
4. Check that logos are clear and readable in both themes

## Current Status

- [ ] `miva_logo_light.png` - Not added yet
- [ ] `miva_logo_dark.png` - Not added yet
- [ ] `miva_logo.png` - Optional fallback

Once you add the logo files, you can delete this instruction file.
