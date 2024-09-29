dict = {
  "Bailey": 21048,
  "Bona": 21049,
  "Campbell": 21050,
  "Clark": 21051,
  "Jaquez": 21052,
}

communicable = {
  "Bailey": ["Bona", "Campbell"],
  "Bona": ["Campbell","Clark","Bailey"],
  "Campbell": ["Jaquez","Bona","Bailey"],
  "Clark": ["Jaquez","Bona"],
  "Jaquez": ["Clark", "Campbell"],
}