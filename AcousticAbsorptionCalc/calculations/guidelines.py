from django.utils.translation import gettext_lazy as _

NORM_GUIDELINES = {
    "school-classroom": _(
        "Use ceiling absorbers with αw ≥ 0.95 across the full surface. Prefer suspended ceilings with air cavity to enhance low-frequency absorption. "
        "Install wall panels (αw ≥ 0.95) at 100–220 cm on the rear wall, and optionally on one side wall. For rooms over 10 m, 60–70% of ceiling coverage is acceptable."
    ),
    "nursery": _(
        "Install ceiling and wall absorbers to reduce reverberation and overall noise levels exceeding 80 dBA. Proper absorption reduces fatigue and improves speech clarity."
    ),
    "common-room": _(
        "Absorption materials should cover walls and ceilings to reduce sound buildup during playtime or mealtime. Aim to lower ambient noise by at least 10 dB."
    ),
    "canteen": _(
        "Use high-performance ceiling absorbers (αw ≥ 0.90) and consider placing panels at children's height to effectively reduce reverberation and echo."
    ),
    "staff-room": _(
        "Provide good acoustic absorption to reduce noise from simultaneous conversations. Aim for calm environment for rest between classes."
    ),
    "technical-room": _(
        "Absorbent ceilings and durable wall panels should be installed to counteract machinery and tool noise, which hinders focus and accelerates fatigue."
    ),
    "cloakroom": _(
        "Install ceiling and high-mounted wall panels to prevent long-distance sound propagation. Effective absorption mitigates stress from noise during breaks."
    ),
    "corridor": _(
        "Use ceiling absorbers (αw = 1.0) to cover 100% of the area. Additional wall panels above 2 m can help reduce echo and noise spread in schools and kindergartens."
    ),
    "stairwell": _(
        "Install absorbers under landings and stair treads. Panels (αw ≥ 0.8) should cover the entire underside surface to meet absorption requirements."
    ),
    "library": _(
        "Use ceiling absorbers (αw ≥ 0.90) for reading rooms and lending zones. At least 50% coverage in open-stack areas. Bookshelves can substitute for wall panels."
    ),
    "courtroom": _(
        "Ensure low reverberation and proper speech clarity with wideband absorbers. Rear wall and ceiling geometry should support even sound distribution."
    ),
    "office": _(
        "Apply ceiling absorbers (αw ≥ 0.90) and optionally carpet or acoustic screens. Wall absorbers (αw ≥ 0.95) recommended above desks or in open spaces."
    ),
    "atrium": _(
        "Distribute high-absorbing materials strategically to reduce excessive echo and reverberation in open, high-volume spaces like foyers and terminals."
    ),
    "gallery": _(
        "Apply ceiling panels to reduce echo in sparsely furnished rooms. Essential for intelligibility and enjoyment of multimedia and exhibitions."
    ),
    "restaurant": _(
        "Balance privacy and speech clarity by using ceiling panels and localized wall panels. Divide large rooms into sections with furnishings if possible."
    ),
    "health-office": _(
        "Short reverberation times increase comfort and speech privacy in medical rooms. Ceiling and wall absorption recommended for both patient and staff well-being."
    ),
    "hospital-ward": _(
        "Use ceiling panels to reduce noise from medical devices and improve conditions for patient rest, communication, and recovery."
    ),
    "waiting-room": _(
        "Limit reverberation and sound propagation. Sound absorption increases speech privacy and reduces stress in medical or public service waiting areas."
    ),
    "hotel-corridor": _(
        "Wall and ceiling absorption is needed to suppress noise spread in long, hard-surfaced corridors in hotels and clinics."
    ),
    "church": _(
        "Solutions must be tailored to the liturgical and architectural context. Carefully plan reverberation time based on room volume and usage."
    ),
}
