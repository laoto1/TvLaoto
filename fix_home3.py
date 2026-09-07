with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# We know the mangled part starts at "// Filter Pills Row" and ends right before "// Channel Items Vertical List"
start_idx = content.find("// Filter Pills Row")
end_idx = content.find("// Channel Items Vertical List")

if start_idx != -1 and end_idx != -1:
    new_block = '''// Filter Pills Row
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        val displayTabs = mutableListOf("Tất cả", "Yêu thích")
                        displayTabs.addAll(dynamicGroups.take(2))
                        
                        if (selectedFilterTab !in displayTabs && selectedFilterTab.isNotBlank()) {
                            if (displayTabs.size > 2) displayTabs[2] = selectedFilterTab
                            else displayTabs.add(selectedFilterTab)
                        }

                        displayTabs.forEach { tab ->
                            val isTabSelected = tab == selectedFilterTab
                            ChannelFilterPill(
                                title = tab,
                                isSelected = isTabSelected,
                                onClick = { 
                                    selectedFilterTab = tab 
                                    scope.launch { repository.saveLastFilterTab(tab) }
                                }
                            )
                        }

                        Box(
                            modifier = Modifier
                                .size(26.dp)
                                .clip(GtaShapes.SmallCardShape)
                                .background(Brush.horizontalGradient(listOf(Color(0x33FFFFFF), Color(0x11FFFFFF))))
                                .border(1.dp, SolidColor(Color(0x33FFFFFF)), GtaShapes.SmallCardShape)
                                .clickable { showAdvancedFilter = true },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Menu,
                                contentDescription = "Bộ lọc",
                                tint = Color.White,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    '''
    content = content[:start_idx] + new_block + content[end_idx:]

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
