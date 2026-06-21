---
name: Epicurean AI
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535a'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb162c'
  secondary: '#f0c12c'
  on-secondary: '#3d2e00'
  secondary-container: '#d2a501'
  on-secondary-container: '#503d00'
  tertiary: '#71d7cf'
  on-tertiary: '#003734'
  tertiary-container: '#32a099'
  on-tertiary-container: '#00302d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffdf90'
  secondary-fixed-dim: '#f0c12c'
  on-secondary-fixed: '#241a00'
  on-secondary-fixed-variant: '#584400'
  tertiary-fixed: '#8ef4eb'
  tertiary-fixed-dim: '#71d7cf'
  on-tertiary-fixed: '#00201e'
  on-tertiary-fixed-variant: '#00504c'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
---

## Brand & Style
The design system is engineered to evoke a sense of high-end culinary curation combined with the precision of advanced intelligence. It targets discerning food enthusiasts who value both aesthetic beauty and functional efficiency. 

The style is a fusion of **Corporate Modern** and **Glassmorphism**. It utilizes a dark-mode-first aesthetic (though adaptable) to create a premium, "night-out" atmosphere. The interface relies on high-contrast typography, expansive whitespace, and translucent layering to establish a sophisticated hierarchy that feels both appetizing and technologically advanced.

## Colors
The palette is anchored by **Deep Charcoal (#121212)** and **Pure White (#FFFFFF)** to ensure maximum legibility and a luxury feel. 

- **Primary Accent:** "Vibrant Tomato Red" (#E23744) is reserved for high-intent actions, primary buttons, and critical active states.
- **Secondary Accent:** "Warm Saffron Gold" (#F4C430) is utilized exclusively for trust signals, such as star ratings, premium badges, and AI-verified markers.
- **Neutrals:** A range of muted greys provides depth for secondary information, borders, and tags, preventing the vibrant accents from overwhelming the content.

## Typography
The system employs a dual-font strategy. **Montserrat** provides an expressive, geometric personality for headlines, echoing the bold branding of high-end editorial food magazines. **Inter** is used for all functional and body text to maintain exceptional readability and a systematic, AI-native feel.

Headlines should use tight tracking and bold weights to command attention, while body text maintains generous line heights for long-form AI insights and restaurant descriptions.

## Layout & Spacing
The layout follows a **Fluid Grid** model with strict 8px increments. 

- **Desktop:** 12-column grid with 24px gutters. Content is centered within a 1280px max-width container.
- **Tablet:** 8-column grid with 20px gutters. 
- **Mobile:** 4-column grid with 16px margins. 

Spacing is used to group related information; for example, restaurant metadata (Cuisine, Rating, Cost) uses `sm` spacing, while distinct sections within a card use `md` spacing to ensure the "AI Insight" feels like a premium, separate layer of value.

## Elevation & Depth
Depth is achieved through **Glassmorphism** and **Ambient Shadows**. 

1.  **Base Layer:** The deepest charcoal background (#121212).
2.  **Card Layer:** Surfaces use a semi-transparent fill (e.g., `rgba(255, 255, 255, 0.05)`) with a `20px` backdrop-blur and a subtle `1px` white border at 10% opacity.
3.  **Elevation:** For hover states or modals, use extra-diffused shadows (`0 20px 40px rgba(0,0,0,0.4)`) with a very slight red tint in the shadow for primary elements to create a "glow" effect.

## Shapes
This design system utilizes a **Rounded** aesthetic to feel approachable and modern. 

- **Standard Elements:** Buttons, input fields, and tags use `0.5rem` (8px).
- **Cards & Containers:** Prominent restaurant cards and AI insight panels use `1rem` (16px) or `1.5rem` (24px) for a softer, more premium appearance.
- **Interactive States:** Buttons may transition to a slightly more rounded state on press to mimic a physical "squish" sensation.

## Components

### Buttons
- **Primary:** Background `#E23744`, white text, Montserrat Bold. High-saturation, used for "Book Now" or "View Menu."
- **Secondary:** Transparent with a `1px` white border.
- **Ghost:** No background, white text, used for less critical actions like "Share" or "Save."

### Cards (The "Epicurean Card")
- **Hierarchy:** Top-aligned Rank (gold badge), followed by a high-resolution food image. Content follows: Name (Headline MD) > Rating/Cuisine (Label MD) > Cost.
- **AI Insight Section:** A distinct, glassmorphic sub-panel at the bottom of the card with a subtle Saffron Gold left-border to highlight personalized recommendations.

### Input Fields
- Sidebar filters and search bars use a dark background (`#1E1E1E`) with a soft `1px` border. On focus, the border glows with the Primary Red.

### Chips & Tags
- Used for cuisines or dietary requirements. Muted grey background (`rgba(255,255,255,0.1)`) with Inter Medium typography.

### Progress & Ratings
- Star ratings use the Saffron Gold. AI "Match Score" uses a circular progress ring in the Primary Red to indicate how well the restaurant fits the user's profile.