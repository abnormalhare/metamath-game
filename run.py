from logic import *

### WFF DEFINITIONS ###

phi = WFF("𝜑")
psi = WFF("𝜓")
chi = WFF("𝜒")
theta = WFF("𝜃")

### METAMATH ###

# Theorem a1ii #

a1ii_1 = Expression(phi)
a1ii_2 = Expression(psi)
a1ii = Theorem("a1ii", Expression(phi), a1ii_1, a1ii_2)

a1ii.substitute(phi, psi)

# Theorem idi #

idi_1 = Expression(phi)
idi = Theorem("idi", Expression(phi), idi_1)

# Syntax Definition wn #

wn = Syntax("¬", lambda var1: not var1)

# Syntax Definition wi #

wi = Syntax("→", lambda var1, var2=None: var1 <= var2)

# Theorem ax-mp #

ax_mp_min = Expression(phi)
ax_mp_maj = Expression(phi, wi, psi)
ax_mp = Theorem("Modus Ponens", Expression(psi), ax_mp_min, ax_mp_maj)

# Theorem ax-1 #

ax_1_wph = Expression(phi)
ax_1_wps = Expression(psi)
ax_1_3 = Expression(ax_1_wps, wi, ax_1_wph)
ax_1_4 = Expression(ax_1_wph, wi, ax_1_3)
ax_1 = Axiom("ax-1", ax_1_wph, ax_1_wps, ax_1_3, ax_1_4)

# Theorem ax-2 #

ax_2_wph = Expression(phi)
ax_2_wps = Expression(psi)
ax_2_wch = Expression(chi)
ax_2_4 = Expression(ax_2_wps, wi, ax_2_wch)
ax_2_5 = Expression(ax_2_wph, wi, ax_2_4)
ax_2_6 = Expression(ax_2_wph, wi, ax_2_wps)
ax_2_7 = Expression(ax_2_wph, wi, ax_2_wch)
ax_2_8 = Expression(ax_2_6, wi, ax_2_7)
ax_2_9 = Expression(ax_2_5, wi, ax_2_8)
ax_2 = Axiom("ax-2", ax_2_wph, ax_2_wps, ax_2_wch, ax_2_4, ax_2_5, ax_2_6, ax_2_7, ax_2_8, ax_2_9)

### TESTING ###

ax_mp.substitute(phi, psi)
ax_mp.test(True, True)

ax_2.substitute(phi, psi, chi)
ax_2.test(True, True, True)