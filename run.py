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

# Theorem idi #

idi_1 = Expression(phi)
idi = Theorem("idi", Expression(phi), idi_1)

# Syntax Definition wn #

wn = Syntax("¬", lambda var1: not var1)

# Syntax Definition wi #

wi = Syntax("→", lambda var1, var2=None: var1 <= var2)

# Axiom ax-mp #

ax_mp_min = Expression(phi)
ax_mp_maj = Expression(phi, wi, psi)
ax_mp = Theorem("ax-mp", Expression(psi), ax_mp_min, ax_mp_maj)

# Axiom ax-1 #

ax_1_wph = Expression(phi)
ax_1_wps = Expression(psi)
ax_1_3 = Expression(ax_1_wps, wi, ax_1_wph)
ax_1_4 = Expression(ax_1_wph, wi, ax_1_3)
ax_1 = Axiom("ax-1", ax_1_wph, ax_1_wps, ax_1_3, ax_1_4)

# Axiom ax-2 #

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

# Axiom ax-3 #

ax_3_wph = Expression(phi)
ax_3_2 = Expression(None, wn, ax_3_wph)
ax_3_wps = Expression(psi)
ax_3_4 = Expression(None, wn, ax_3_wps)
ax_3_5 = Expression(ax_3_2, wi, ax_3_4)
ax_3_6 = Expression(ax_3_wps, wi, ax_3_wph)
ax_3_7 = Expression(ax_3_5, wi, ax_3_6)
ax_3 = Axiom("ax-3", ax_3_wph, ax_3_2, ax_3_wps, ax_3_4, ax_3_5, ax_3_6, ax_3_7)

mp2_2 = Expression(psi)
mp2_1 = Expression(phi)
mp2_3a = Expression(psi, wi, chi)
mp2_3 = Expression(phi, wi, mp2_3a)
mp2 = Theorem("mp2", Expression(chi), mp2_1, mp2_2, mp2_3, [ax_mp, mp2_3], [ax_mp, 4])

### TESTING ###

ax_mp.substitute(phi, psi)
ax_mp.test(True, True)

ax_2.substitute(phi, psi, chi)
ax_2.test(True, True, True)

ax_3.substitute(phi, psi)
ax_3.test(True, True)

mp2.substitute(phi, psi, chi)