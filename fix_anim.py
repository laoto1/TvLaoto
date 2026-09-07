import re

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

new_imports = """import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.Spring"""
if "scaleIn" not in content:
    content = content.replace("import androidx.compose.animation.togetherWith", "import androidx.compose.animation.togetherWith\n" + new_imports)

# Replace the AnimatedContent transition
old_anim = """                    (fadeIn(animationSpec = tween(300))
                    ).togetherWith(fadeOut(animationSpec = tween(300)))"""
new_anim = """                    (fadeIn(animationSpec = tween(200)) + scaleIn(
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

content = content.replace(old_anim, new_anim)

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated animation in ProgramInfoPanel.kt")
