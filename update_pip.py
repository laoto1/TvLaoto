import re

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import com.tvlaoto.ui.theme.neonBorder',
'''import com.tvlaoto.ui.theme.neonBorder
import com.tvlaoto.data.model.EpgProgram''')

target = '''@Composable
fun ProgramInfoPanel(
    channel: IptvChannel?,
    onReplayClick: () -> Unit,
    onFavoriteClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    if (channel == null) return

    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(top = 14.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Left Column: Program Title, Time, Description
        Column(modifier = Modifier.weight(1f).padding(end = 16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = channel.currentProgram,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 20.sp,
                        color = Color.White
                    )
                )
                Spacer(modifier = Modifier.width(10.dp))
                Box(
                    modifier = Modifier
                        .clip(GtaShapes.TagShape)
                        .background(Color(0xFFEC4899))
                        .padding(horizontal = 7.dp, vertical = 2.dp)
                ) {
                    Text(
                        text = "LIVE",
                        style = TextStyle(
                            fontFamily = FontFamily.SansSerif,
                            fontWeight = FontWeight.Bold,
                            fontSize = 9.sp,
                            color = Color.White
                        )
                    )
                }
            }
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = "Đang phát sóng",
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = FontWeight.Normal,
                    fontSize = 14.sp,
                    color = GtaColors.TextSecondary
                )
            )
        }'''

replacement = '''@Composable
fun ProgramInfoPanel(
    channel: IptvChannel?,
    currentCatchupProgram: EpgProgram?,
    liveProgram: EpgProgram?,
    onReplayClick: () -> Unit,
    onFavoriteClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    if (channel == null) return

    val title = currentCatchupProgram?.title ?: liveProgram?.title ?: channel.currentProgram.takeIf { it.isNotBlank() } ?: "Trực tiếp"
    val time = currentCatchupProgram?.time ?: liveProgram?.time ?: "Đang phát sóng"
    val isLive = currentCatchupProgram == null

    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(top = 14.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Left Column: Program Title, Time, Description
        Column(modifier = Modifier.weight(1f).padding(end = 16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = title,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 20.sp,
                        color = Color.White
                    )
                )
                if (isLive) {
                    Spacer(modifier = Modifier.width(10.dp))
                    Box(
                        modifier = Modifier
                            .clip(GtaShapes.TagShape)
                            .background(Color(0xFFEC4899))
                            .padding(horizontal = 7.dp, vertical = 2.dp)
                    ) {
                        Text(
                            text = "LIVE",
                            style = TextStyle(
                                fontFamily = FontFamily.SansSerif,
                                fontWeight = FontWeight.Bold,
                                fontSize = 9.sp,
                                color = Color.White
                            )
                        )
                    }
                }
            }
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = time,
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = FontWeight.Normal,
                    fontSize = 14.sp,
                    color = GtaColors.ElectricCyan
                )
            )
        }'''

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated ProgramInfoPanel.kt")
else:
    print("Target not found in ProgramInfoPanel.kt")

