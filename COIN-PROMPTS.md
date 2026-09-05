# Six prompts to paste into ChatGPT

One message each, in a fresh chat. Paste the block, download the image it gives
you, and keep going. Don't rename anything — the filename doesn't matter.

When you have all six, drop them into the chat with me and I'll cut out the
backgrounds, punch the two holes, square them up and commit them. That step is
already built (`tools/prepare_coins.py`); you don't run it.

**Why white and not transparent:** ChatGPT's image generation won't reliably
give you a transparent PNG from the chat window. So these ask for a flat white
background instead, which I remove afterwards. That's why every prompt insists
on *no shadow* — a drop shadow is the one thing that makes the cutout messy.

---

## 1 · Jordan

```
A square macro product photograph of a single circular coin, shot straight down
from directly above. The coin is perfectly centred and circular, filling about
85% of the frame.

The background is a completely flat, uniform pure white — no gradient, no
vignette, no texture, no drop shadow, no reflection, and nothing else in the
frame at all. The coin appears to float on plain white.

The coin is golden nickel-brass, a warm brassy tone, with a finely reeded
milled edge. Raised sans-serif capital letters arch across the top of the face
reading JORDAN, and across the bottom reading DINAR. In the centre, large and
in high relief, is the Eastern Arabic numeral ١٠. A plain raised circular
border rings the inner field.

It is a coin that has been in circulation: fine hairline scratches across the
flat field, softened high points on the lettering, faint darkened patina
settled into the engraving. Soft diffuse studio light from the upper left gives
gentle specular highlights on the raised relief and shallow shading in the
recesses. Sharp macro focus edge to edge. Shallow relief, struck rather than
engraved. No text anywhere outside the coin itself.
```

## 2 · Philippines

```
A square macro product photograph of a single circular coin, shot straight down
from directly above. The coin is perfectly centred and circular, filling about
85% of the frame.

The background is a completely flat, uniform pure white — no gradient, no
vignette, no texture, no drop shadow, no reflection, and nothing else in the
frame at all. The coin appears to float on plain white.

The coin is bright nickel-plated steel, a cool silver-white, with a smooth
plain edge. Raised sans-serif capital letters arch across the top of the face
reading PHILIPPINES, and across the bottom reading PISO. In the centre, large
and in high relief, is the numeral 1. A plain raised circular border rings the
inner field.

It is a coin that has been in circulation: fine hairline scratches across the
flat field, softened high points on the lettering, faint darkened patina
settled into the engraving. Soft diffuse studio light from the upper left gives
gentle specular highlights on the raised relief and shallow shading in the
recesses. Sharp macro focus edge to edge. Shallow relief, struck rather than
engraved. No text anywhere outside the coin itself.
```

## 3 · Papua New Guinea

```
A square macro product photograph of a single circular coin, shot straight down
from directly above. The coin is perfectly centred and circular, filling about
85% of the frame.

The background is a completely flat, uniform pure white — no gradient, no
vignette, no texture, no drop shadow, no reflection, and nothing else in the
frame at all. The coin appears to float on plain white.

The coin is aged silver-grey cupronickel, noticeably darker and more oxidised
than a new coin, with a reeded edge. A perfectly round hole is punched straight
through the exact centre of the coin, and the same flat white background shows
through that hole. A raised rim surrounds the hole. Raised sans-serif capital
letters arch across the top of the face reading PAPUA NEW GUINEA, and across
the bottom reading KINA.

It is a coin that has been in circulation: fine hairline scratches across the
flat field, softened high points on the lettering, faint darkened patina
settled into the engraving. Soft diffuse studio light from the upper left gives
gentle specular highlights on the raised relief and shallow shading in the
recesses. Sharp macro focus edge to edge. Shallow relief, struck rather than
engraved. No text anywhere outside the coin itself.
```

## 4 · Thailand

```
A square macro product photograph of a single circular coin, shot straight down
from directly above. The coin is perfectly centred and circular, filling about
85% of the frame.

The background is a completely flat, uniform pure white — no gradient, no
vignette, no texture, no drop shadow, no reflection, and nothing else in the
frame at all. The coin appears to float on plain white.

The coin is bimetallic: a white cupronickel outer ring around a warm brass-gold
centre disc, with a clean visible seam between the two metals. Raised sans-serif
capital letters arch across the white outer ring, reading THAILAND at the top
and BAHT at the bottom. In the brass centre, large and in high relief, is the
Thai numeral ๑๐.

It is a coin that has been in circulation: fine hairline scratches across the
flat field, softened high points on the lettering, faint darkened patina
settled into the engraving. Soft diffuse studio light from the upper left gives
gentle specular highlights on the raised relief and shallow shading in the
recesses. Sharp macro focus edge to edge. Shallow relief, struck rather than
engraved. No text anywhere outside the coin itself.
```

## 5 · Germany

```
A square macro product photograph of a single circular coin, shot straight down
from directly above. The coin is perfectly centred and circular, filling about
85% of the frame.

The background is a completely flat, uniform pure white — no gradient, no
vignette, no texture, no drop shadow, no reflection, and nothing else in the
frame at all. The coin appears to float on plain white.

The coin is bimetallic: a gold-coloured nickel-brass outer ring around a silver
cupronickel centre disc, with a clean visible seam between the two metals.
Raised sans-serif capital letters arch across the gold outer ring, reading
GERMANY at the top and EURO at the bottom. In the silver centre, large and in
high relief, is the numeral 2.

It is a coin that has been in circulation: fine hairline scratches across the
flat field, softened high points on the lettering, faint darkened patina
settled into the engraving. Soft diffuse studio light from the upper left gives
gentle specular highlights on the raised relief and shallow shading in the
recesses. Sharp macro focus edge to edge. Shallow relief, struck rather than
engraved. No text anywhere outside the coin itself.
```

## 6 · Denmark

```
A square macro product photograph of a single circular coin, shot straight down
from directly above. The coin is perfectly centred and circular, filling about
85% of the frame.

The background is a completely flat, uniform pure white — no gradient, no
vignette, no texture, no drop shadow, no reflection, and nothing else in the
frame at all. The coin appears to float on plain white.

The coin is silver cupronickel with a reeded edge. A perfectly round hole is
punched straight through the exact centre of the coin, and the same flat white
background shows through that hole. Above the hole sits a crowned royal
monogram in raised relief: a simple heraldic crown over an entwined cipher.
Raised sans-serif capital letters arch across the top of the face reading
DENMARK, and across the bottom reading KRONE.

It is a coin that has been in circulation: fine hairline scratches across the
flat field, softened high points on the lettering, faint darkened patina
settled into the engraving. Soft diffuse studio light from the upper left gives
gentle specular highlights on the raised relief and shallow shading in the
recesses. Sharp macro focus edge to edge. Shallow relief, struck rather than
engraved. No text anywhere outside the coin itself.
```

---

## When it goes wrong

**A drop shadow crept in.** This is the one that actually matters — it leaves a
grey halo after the cutout. Reply: *"Same coin, but remove the shadow entirely.
The background must be pure flat white with nothing on it."*

**The lettering is misspelled.** Expected, especially `١٠` and `๑๐`. Reply:
*"The lettering is wrong. Redo it with the text spelled exactly: JORDAN across
the top, DINAR across the bottom."* Copy the numerals from this file rather
than retyping them.

**It's still wrong after two tries.** Take the better path instead: ask for
*"the same coin with a completely blank raised inner field and no lettering
anywhere on it"*, and send me that. I'll set the legend and the denomination as
crisp vector type on top — which will read better than anything the model
letters by hand, and stays sharp at any size.

**The background isn't quite white.** Doesn't matter. The cutout samples the
actual corner colour, so a warm off-white or a light grey works as long as it's
*flat*.
