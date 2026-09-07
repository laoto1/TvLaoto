import re

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

old_anim = """                    (fadeIn(animationSpec = tween(200)) + scaleIn(
                        animationSpec = spring(
                            dampingRatio = Spring.DampingRatioMediumBouncy,
                            stiffness = Spring.StiffnessLow
                        ),
                        initialScale = 0.8f
                    )).togetherWith(
                        fadeOut(animationSpec = tween(200)) + scaleOut(
                            animationSpec = tween(200),
                            targetScale = 0.8f
                        )
                    )"""
                    
new_anim = """                    (fadeIn(animationSpec = tween(300))
                    ).togetherWith(fadeOut(animationSpec = tween(300)))"""

content = content.replace(old_anim, new_anim)

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Reverted to fade animation in ProgramInfoPanel.kt")
