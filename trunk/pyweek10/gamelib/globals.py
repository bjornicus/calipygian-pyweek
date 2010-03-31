SECONDS_TO_CROSS_SCREEN = 4

# Entity type flags
(
    ENTITY_STATIC, # Entity only gets called for Drawing
    ENTITY_ACTOR,  # Entity is drawn and receives tick calls
    ENTITY_REACTOR # Entity is drawn, receives tick calls and keyboard state
) = range(3)