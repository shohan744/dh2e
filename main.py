import random
import re
import textwrap

# Homeworld data
homeworlds = {
    'Feral World': {
        'description': 'The eternal struggle of primitive forces molded you from a young age.',
        'advantages': ['Strength', 'Toughness'],
        'disadvantages': ['Influence'],
        'aptitude': 'Toughness',
        'base_fate': 2,
        'base_wounds': 9,
        'unique_bonus': 'The Old Ways: Low-Tech weapons lose Primitive Quality and gain Proven (3).'
    },
    'Hive World': {
        'description': 'The eternal buzz of the hive world molded your upbringing.',
        'advantages': ['Agility', 'Perception'],
        'disadvantages': ['Willpower'],
        'aptitude': 'Perception',
        'base_fate': 2,
        'base_wounds': 8,
        'unique_bonus': 'Teeming Masses in Metal Mountains: Move through crowds as open terrain, +20 to Navigate (Surface) in closed spaces.'
    },
    'Forge World': {
        'description': 'From birth, you were a cog in the Omnissiah-blessed war machine.',
        'advantages': ['Intelligence', 'Toughness'],
        'disadvantages': ['Fellowship'],
        'aptitude': 'Intelligence',
        'base_fate': 3,
        'base_wounds': 8,
        'unique_bonus': 'Omnissiah\'s Chosen: Gain Technical Knock or Weapon-Tech Talent.'
    },
    'Highborn World': {
        'description': 'As you developed among the nobility, you learned politics could kill like bolt-shot.',
        'advantages': ['Fellowship', 'Influence'],
        'disadvantages': ['Toughness'],
        'aptitude': 'Fellowship',
        'base_fate': 4,
        'base_wounds': 9,
        'unique_bonus': 'Breeding Counts: Reduce Influence losses by 1, to a minimum loss of 1.'
    },
    'Shrine World': {
        'description': 'You matured in the palm of His hand, a seat of holy power.',
        'advantages': ['Fellowship', 'Willpower'],
        'disadvantages': ['Perception'],
        'aptitude': 'Willpower',
        'base_fate': 3,
        'base_wounds': 8,
        'unique_bonus': 'Faith in the Creed: When spending a Fate Point, it is not reduced on a 1d10 result of 1.'
    },
    'Voidborn': {
        'description': 'The warpway was your home, an endless expanse of void and chaos.',
        'advantages': ['Intelligence', 'Willpower'],
        'disadvantages': ['Strength'],
        'aptitude': 'Intelligence',
        'base_fate': 3,
        'base_wounds': 7,
        'unique_bonus': 'Child of the Dark: Start with Strong Minded talent, +30 to tests in zero-gravity.'
    },
    'Agri-World': {
        'description': 'For years, your shoulders held the responsibility for feeding billions of kin.',
        'advantages': ['Fellowship', 'Strength'],
        'disadvantages': ['Agility'],
        'aptitude': 'Strength',
        'base_fate': 2,
        'base_wounds': 8,
        'unique_bonus': 'Strength from the Land: Start with Brutal Charge (2) trait.'
    }
}
        #Background Data
backgrounds = {
    'Adeptus Administratum': {
        'description': 'You were but one being in the never-ending Adeptus Administratum, an expansive giga-bureaucracy that forms the backbone of the Imperium.',
        'starting_skills': 'Commerce or Medicine; Common Lore (Adeptus Administratum); Linguistics (High Gothic); Logic; Scholastic Lore (Choose Subject)',
        'starting_equipment': 'Laspistol or Stub Automatic; Imperial Robes; Autoquill; Chrono; Dataslate; Medi-kit',
        'starting_talents': 'Weapon Training (Las) or Weapon Training (Solid Projectile)',
        'starting_aptitudes': 'Knowledge or Social',
        'background_bonus': 'Master of Paperwork: An Adeptus Administratum character counts the Availability of all items as one level more available (Very Rare items count as Rare, Average items count as Common, etc.).'
    },
    'Adeptus Arbites': {
        'description': 'As a member of the Adeptus Arbites, you oversaw the brutal execution of the Imperium justice.',
        'starting_skills': 'Awareness; Common Lore (Adeptus Arbites; Underworld); Inquiry or Interrogation; Intimidate; Scrutiny',
        'starting_equipment': 'Shotgun or Shock Maul; Enforcer Light Carapace Armour or Carapace Chest Plate; 3 doses of Stimm; Manacles; 12 Lho Sticks',
        'starting_talents': 'Weapon Training (Shock) or Weapon Training (Solid Projectile)',
        'starting_aptitudes': 'Offense or Defense',
        'background_bonus': 'The Face of the Law: An Arbitrator can substitute his Willpower bonus for his degrees of success on intimidation and Interrogation tests.'
    },
    'Adeptus Astra Telepathica': {
        'description': 'Psykers like you were kept tightly guarded within the Adeptus Astra Telepathica, for your Warp-born powers could doom whole systems.',
        'starting_skills': 'Awareness; Common Lore (Adeptus Astra Telepathica); Deceive or Interrogation; Forbidden Lore (the Warp); Psyniscience or Scrutiny',
        'starting_equipment': 'Laspistol, Staff or Whip, Light Flak Cloak or Flak Vest, Micro-bead or Psy Focus',
        'starting_talents': 'Weapon Training (Las, Low-Tech)',
        'starting_aptitudes': 'Defense or Psyker',
        'background_bonus': 'The Constant Threat: Increase or decrease the result by an amount equal to his Willpower bonus when triggering a roll on the Psychic Phenomenon table.'
    },
    'Adeptus Mechanicus': {
        'description': 'In an era of infinite ignorance, you and your kin in the Adeptus Mechanicus jealously guarded ancient knowledge.',
        'starting_skills': 'Awareness or Operate (Choose Vehicle); Common Lore (Adeptus Mechanicus); Logic; Security; Tech',
        'starting_equipment': 'Autogun or Hand Cannon; Monotask Servo-skull or Optical Mechadendrite; Imperial Robes; 2 vials of Sacred Unguents',
        'starting_talents': 'Mechadendrite Use (Utility); Weapon Training (Solid Projectile)',
        'starting_aptitudes': 'Knowledge or Tech',
        'background_bonus': 'Replace the Weak Flesh: Count the Availability of all cybernetics as two levels more available.'
    },
'Adeptus Ministorum': {
    'description': 'As a member of the Adeptus Ministorum, your life was dedicated to the ecclesiarchy and the worship of the God-Emperor.',
    'starting_skills': 'Charm; Command; Common Lore (Adeptus Ministorum); Inquiry or Scrutiny; Linguistics (High Gothic)',
    'starting_equipment': 'Hand Flamer or Warhammer and Stub Revolver; Imperial Robes or Flak Vest; Backpack; Glow-globe; Monotask Servo-skull (Laud hailer)',
    'starting_talents': 'Weapon Training (Flame) or Weapon Training (Low-Tech, Solid Projectile)',
    'starting_aptitudes': 'Leadership or Social',
    'background_bonus': 'Faith is All: When spending a Fate point to gain a +10 bonus to any one test, an Adeptus Ministorum character gains a +20 bonus instead.'
},
'Imperial Guard': {
    'description': 'As a former soldier in the Imperial Guard, you served as the hammer of the Emperor, bringing his wrath to the enemies of mankind.',
    'starting_skills': 'Athletics; Command; Common Lore (Imperial Guard); Medicae or Operate (Surface); Navigate (Surface)',
    'starting_equipment': 'Lasgun (or Laspistol and Sword); Combat Vest; Imperial Guard Flak Armour; Grapnel and line; 12 Lho Sticks; Magnoculars',
    'starting_talents': 'Weapon Training (Las, Low-Tech)',
    'starting_aptitudes': 'Fieldcraft or Leadership',
    'background_bonus': 'Hammer of the Emperor: When attacking a target that an ally attacked since the end of the Guardsman\'s last turn, the Guardsman can re-roll any results of 1 or 2 on damage rolls.'
},
'Outcast': {
    'description': 'Living on the fringes of the Imperium society, you learned to rely on yourself in the lawless parts of the galaxy.',
    'starting_skills': 'Acrobatics or Sleight of Hand; Common Lore (Underworld); Deceive; Dodge; Stealth',
    'starting_equipment': 'Autopistol or Laspistol; Chainsword; Armoured Body Glove or Flak Vest; Injector; 2 doses of Obscura or 2 doses of Slaught',
    'starting_talents': 'Weapon Training (Chain); Weapon Training (Las) Weapon Training (Solid Projectile)',
    'starting_aptitudes': 'Fieldcraft or Social',
    'background_bonus': 'Never Quit: An Outcast character counts his Toughness bonus as two higher for purposes of determining Fatigue.'
},
'Adepta Sororitas': {
    'description': 'As a member of the Adepta Sororitas, you were part of an elite sisterhood sworn to defend the Ecclesiarchy and the Imperial Creed.',
    'starting_skills': 'Athletics; Charm or Intimidate; Common Lore (Adepta Sororitas); Linguistics (High Gothic); Medicae or Parry',
    'starting_equipment': 'Hand flamer or laspistol; chainblade; armoured bodyglove; chrono; dataslate; stablight; micro-bead',
    'starting_talents': 'Weapon Training Flame or Weapon Training Las or Weapon Training Chain',
    'starting_aptitudes': 'Offense or Social',
    'background_bonus': 'Incorruptible Devotion: Whenever an Adepta Sororitas character would gain 1 or more Corruption Points, she gains that many Insanity Points minus 1 (to a minimum of 0) instead.'
}
}
#Roles Data
roles = {
    'Assassin': {
        'Description': 'In an age of carnage, you turn bloodshed into an art form. The assassin is one who is always looking to refine their killing technique.',
        'Role Aptitudes': 'Agility, Ballistic Skill or Weapon Skill, Fieldcraft, Finesse, Perception',
        'Role Talents': 'Jaded or Leap Up',
        'Role Bonus': 'Sure Kill: In addition to the normal uses of Fate points, when an Assassin successfully hits with an attack, he may spend a Fate point to inflict additional damage equal to his degrees of success on the attack roll on the first hit the attack inflicts.'
    },
    'Chirurgeon': {
        'Description': 'Medical knowledge is as closely guarded as mechanical within the Imperium. The flesh-sculpting chirurgeon is both feared and respected.',
        'Role Aptitudes': 'Fieldcraft, Intelligence, Knowledge, Strength, Toughness',
        'Role Talents': 'Resistance (Choose Type) or Takedown',
        'Role Bonus': 'Dedicated Healer: In addition to the normal uses of Fate points, when a Chirurgeon character fails a test to provide First Aid, he can spend a Fate point to automatically succeed instead with the degrees of success equal to his Intelligence bonus.'
    },
    'Desperado': {
        'Description': 'Renegades, iconoclasts, bounty hunters - all men and women who live by grit and trigger are known as Desperados.',
        'Role Aptitudes': 'Agility, Ballistic Skill, Defense, Fellowship, Finesse',
        'Role Talents': 'Catfall or Quick Draw',
        'Role Bonus': 'Move and Shoot: Once per round, after performing a Move action, a Desperado character may perform a single Standard Attack with a Pistol weapon he is currently wielding as a Free Action.'
    },
    'Hierophant': {
        'Description': 'Demagoguery and zealous fire light the path of the Hierophant. Do you have the strength to serve in the Cult of the Emperor?',
        'Role Aptitudes': 'Fellowship, Offence, Social, Toughness, Willpower',
        'Role Talents': 'Double Team or Hatred (Pick Group)',
        'Role Bonus': 'Sway the Masses: In addition to the normal uses of Fate points, a Hierophant character may spend a Fate point to automatically succeed at a Charm, Command, or Intimidate skill test with a number of degrees of success equal to his Willpower bonus.'
    },
    'Mystic': {
        'Description': 'Your warp-touched mind has seen beyond mortal comprehension, elevating you to the status of a Mystic.',
        'Role Aptitudes': 'Defense, Intelligence, Knowledge, Perception, Willpower',
        'Role Talents': 'Resistance (Psychic Powers) or Warp Sense',
        'Role Bonus': 'Stare into the Warp: A Mystic character starts the game with the Psyker elite advance. It is recommended that a character who wishes to be a Mystic have a Willpower of at least 35.'
    },
    'Sage': {
        'Description': 'Mankind has lost and gained eons of knowledge over the centuries - you, who specialize in the recovery and preservation of that knowledge, are known as Sages.',
        'Role Aptitudes': 'Intelligence, Knowledge, Perception, Tech, Willpower',
        'Role Talents': 'Ambidextrous or Clues from the Crowds',
        'Role Bonus': 'Quest for Knowledge: In addition to the normal uses of Fate points, a Sage character may spend a Fate point to automatically succeed at a Logic or any Lore skill test with a number of degrees of success equal to his Intelligence bonus.'
    },
    'Seeker': {
        'Description': 'The thrill of the hunt. The satisfaction of investigation. Attention and obsession. This is what drives you, Seeker.',
        'Role Aptitudes': 'Fellowship, Intelligence, Perception, Social, Tech',
        'Role Talents': 'Keen Intuition or Disarm',
        'Role Bonus': 'Nothing Escapes My Sight: In addition to the normal uses of Fate points, a Seeker character may spend a Fate point to automatically succeed at an Awareness or Inquiry skill test with a number of degrees of success equal to his Perception bonus.'
    },
}

twist_of_fate_table = {
    1: {
        "description": "There are no answers. Only Death.",
        "effect": "Lose 1 Fate Threshold"
    },
    2: {
        "description": "Flesh is the soul’s mirror. By their misshapen forms will you know their heresy.",
        "effect": "Roll once on Mutations and apply the result."
    },
    3: {
        "description": "Mutation without, corruption within.",
        "effect": "Roll once on Malignancies and apply the result."
    },
    4: {
        "description": "Sins hidden in the heart turn all to decay.",
        "effect": "Gain 3 Corruption Points."
    },
    5: {
        "description": "Trust Not the Soulless Machine.",
        "effect": "This character treats all weapons more complicated than Low-Tech with a (-10) penalty for their use."
    },
    6: {
        "description": "Trust in your fear.",
        "effect": "Gain 5 Perception, Gain Minor Mental Disorder 'Phobia'."
    },
    7: {
        "description": "Death is but a doorway.",
        "effect": "When this character Burns a Fate Point to survive, they gain their original Fate Threshold in Insanity Points."
    },
    8: {
        "description": "By slaying the body we may yet save the soul.",
        "effect": "If this character has a Corruption Bonus of one or higher then they take a further (-10) penalty to tests involving Critical wounds."
    },
    9: {
        "description": "Beyond the Imperium is only darkness and heresy.",
        "effect": "While this character is traveling in the void or warp they take a (-10) penalty to Willpower tests."
    },
    10: {
        "description": "Innocence may mask the quintessence of horrors.",
        "effect": "If this character's Corruption Bonus is not equal to their Fellowship Bonus they take a (-10) to Charm and Deceive tests."
    },
    11: {
        "description": "They that wallow in sin deserve not the mercy of the pyre.",
        "effect": "If this character has a Malediction or Mutation, they take (-10) to resisting tests related to Flame Trait attacks."
    },
    12: {
        "description": "The pain of the bullet is ecstasy compared to damnation.",
        "effect": "Lose 3 Agility. The first time this character suffers Critical damage each session, roll 1d10. On a 10, they do not suffer any Critical Effects, though the damage still counts as Critical damage."
    },
    13: {
        "description": "Humans must die so that humanity can endure.",
        "effect": "Gain Jaded talent. If you already have this talent, Gain 2 Willpower."
    },
    14: {
        "description": "He who hesitates is damned.",
        "effect": "Gain 3 Agility OR Gain 3 Perception. Lose 3 Toughness OR Lose 3 Intelligence."
    },
    15: {
        "description": "Faith in the Emperor is the only true armor a warrior needs.",
        "effect": "Gain Deny the Witch talent. If you already have this talent, Gain 2 Willpower."
    },
    16: {
        "description": "Be a boon to your allies and the bane of your enemies.",
        "effect": "This character gains the Hatred talent. If you already have this talent, Gain 2 Strength."
    },
    17: {
        "description": "Hard work conquers everything.",
        "effect": "Gain the Hardy talent. If you already have this talent, Gain 2 Toughness."
    },
    18: {
        "description": "Pray earnestly for your tech-devices.",
        "effect": "Gain the Tech Use skill (Rank 1). If you already have this skill, Gain 2 Intelligence."
    },
    19: {
        "description": "The wise learn from the deaths of others.",
        "effect": "Gain 3 Agility OR Gain 3 Intelligence. Lose 3 Ballistic Skill OR Lose 3 Weapon Skill."
    },
    20: {
        "description": "Every man is a spark in the darkness.",
        "effect": "Characters (NPC or PC) take a (-10) to any tests to recognize or recall this PC's existence for any reason."
    },
    21: {
        "description": "Only the guilty fear tomorrow.",
        "effect": "Gain the Scrutiny skill (Rank 1) . If you already have this skill, Gain 2 Perception."
    },
    22: {
        "description": "The heretic unchecked wreaks havoc among the faithful.",
        "effect": "For the rest of an encounter or scene, after this character Spends or Burns a Fate Point, they take a (-10) to Resistance Tests that would result in gaining Corruption Points."
    },
    23: {
        "description": "To Question your Duty is to Fail your Duty.",
        "effect": "If this character is acting following a Command, then increase the bonus by a further (+10)."
    },
    24: {
        "description": "Kill the alien before it can speak its lies.",
        "effect": "Gain the Quick Draw talent. If you already have this talent, Gain 2 Agility."
    },
    25: {
        "description": "Better an eternal martyr than a coward for one instant.",
        "effect": "Gain the One-on-One talent. If you already have this talent, Gain 2 Weapon Skill."
    },
    26: {
        "description": "Know the mutant; kill the mutant.",
        "effect": "Gain 2 Perception."
    },
    27: {
        "description": "Mourn not the Martyr; give praise instead for such sacrifice.",
        "effect": "Gain the Bodyguard talent. If you already have this talent, Gain 2 Agility."
    },
    28: {
        "description": "Wise is he who does not question.",
        "effect": "Gain the Archivator talent. If you already have this talent, Gain 2 Intelligence."
    },
    29: {
        "description": "Truth is subjective.",
        "effect": "Gain 3 Perception. The first time they would gain 1 or more Corruption points each session, they gain that amount plus 1 instead."
    },
    30: {
        "description": "For every battle honor, a thousand heroes die alone.",
        "effect": "Gain 5 Fellowship. Gain Minor Mental Disorder 'Visions and Voices'"
    },
    31: {
        "description": "Thought begets Heresy.",
        "effect": "Lose 3 Intelligence. The first time they would gain 1 or more Corruption points each session, they reduce that amount by 1 (to a minimum of 0) instead."
    },
    32: {
        "description": "Heresy begets Retribution.",
        "effect": "Gain 3 Fellowship OR Gain 3 Strength. Lose 3 Toughness OR Lose 3 Willpower."
    },
    33: {
        "description": "Heresy is the Child of Free Thought.",
        "effect": "Tests to resist Interaction skills against this character are one degree more difficult."
    },
    34: {
        "description": "He who serves best obeys without question.",
        "effect": "Gain the Command skill (Rank) 1. If you already have this skill, Gain 2 Fellowship."
    },
    35: {
        "description": "Success is commemorated; Failure merely remembered.",
        "effect": "Gain the Grenadier talent. If you already have this talent, Gain 2 Ballistic Skill."
    },
    36: {
        "description": "Seek not honor for your sacrifice; the Emperor sees all.",
        "effect": "This character gains the Peer (GM’s discretion) talent. Lose 2 Toughness."
    },
    37: {
        "description": "Toil for the Emperor earns redemption; suffering for the Emperor earns piety.",
        "effect": "Gain the Flagellant talent. If you already have this talent, Gain 2 Toughness."
    },
    38: {
        "description": "The worst enemies are those we make ourselves.",
        "effect": "This character gains the Enemy (GM’s discretion) talent. They also gain the Hatred talent for the same faction."
    },
    39: {
        "description": "Ignorance is a blessing not to be disdained by the wise",
        "effect": "Gain the Cover-Up talent. If you already have this talent, Gain 2 Intelligence."
    },
    40: {
        "description": "It is not in my mind to ask questions that cannot be answered.",
        "effect": "Gain 5 Intelligence. Gain Minor Mental Disorder 'Obsession/Compulsion'"
    },
    41: {
        "description": "A mind without purpose wanders in dark places.",
        "effect": "When gaining Mental Disorders, this character must choose to gain a new Disorder instead of increasing the severity of an existing Disorder."
    },
    42: {
        "description": "Stand not between Inquisitor and heretic.",
        "effect": "Gain the Hard Target talent. If you already have this talent, Gain 2 Toughness."
    },
    43: {
        "description": "The foolish man puts his trust in luck, the wise man puts his trust in the Emperor.",
        "effect": "Gain the Catfall talent. If you already have this talent, Gain 2 Agility."
    },
    44: {
        "description": "Fates worse than death are the just reward of the curious.",
        "effect": "Whenever this character gains a new Lore skill they also gain one Insanity Point. Going over an Insanity Point threshold in this manner does not trigger Shock."
    },
    45: {
        "description": "If a job is worth doing, it is worth dying for.",
        "effect": "Gain 3 Toughness OR Gain 3 Willpower. Lose 3 Fellowship OR Lose 3 Strength."
    },
    46: {
        "description": "Revulsion is a message from the God-Emperor.",
        "effect": "When this character is making a Fear test due to natural means they gain a (+10) on the next immediate test following the resolution of the Fear Test."
    },
    47: {
        "description": "The justice of the Imperium can be found at the tip of a bolt shell.",
        "effect": "Gain the Weapon Training talent (Las, Low-tech, or Solid Projectile). If you have all three talents Gain 2 Ballistic Skill OR Gain 2 Weapon Skill instead."
    },
    48: {
        "description": "Trust only the Emperor, for all others are suspect.",
        "effect": "Gain the Double Team talent. If you already have this talent, Gain 2 Weapon Skill."
    },
    49: {
        "description": "“There are no civilians in the battle for survival.”",
        "effect": "Gain 2 Toughness AND Gain 1 Wound."
    },
    50: {
        "description": "There is no right or wrong in our profession.",
        "effect": "If this character spends a Fate Point to reroll a test, have them make a Challenging (+0) Willpower test. If they fail they are stunned with indecision for the round, and the Fate Point is not spent."
    },
    51: {
        "description": "Dishonour your war-gear and it will fail you.",
        "effect": "Gain the Technical Knock talent. If you already have this talent, Gain 2 Intelligence."
    },
    52: {
        "description": "When in doubt, advance towards the sound of the guns.",
        "effect": "Gain the Athletics skill (Rank 1). If you already have this skill, Gain 2 Perception."
    },
    53: {
        "description": "Dark dreams lie upon the heart.",
        "effect": "Whenever this character would roll Malignancies, they may instead select any one result and gain that Malignancy."
    },
    54: {
        "description": "Only the insane have strength enough to prosper.",
        "effect": "Gain 3 Willpower. The first time they would gain 1 or more Insanity points each session, they gains that amount plus 1 instead."
    },
    55: {
        "description": "Only those who prosper may judge what is sane.",
        "effect": "Lose 3 Willpower. This character lowers their Fellowship by (-10) when interacting with individuals with less Insanity Points than themselves."
    },
    56: {
        "description": "Violence solves everything.",
        "effect": "Gain 3 Weapom Skill OR Gain 3 Ballistic Skill. Lose 3 Agility OR Lose 3 Intelligence."
    },
    57: {
        "description": "Let your Faith in the Emperor be the Flame that burns the Heretic.",
        "effect": "Gain the Counter Attack talent. If you already have this talent, Gain 2 Weapon Skill."
    },
    58: {
        "description": "Die if you must, but not with your spirit broken.",
        "effect": "Gain 3 Willpower."
    },
    59: {
        "description": "The sword that you sharpen can be turned on you.",
        "effect": "Gains the Whirlwind of Death Talent. If you already have this talent, Gain 2 Weapon Skill."
    },
    60: {
        "description": "The Rewards of Tolerance are Treachery and Betrayal.",
        "effect": "Gain the Ambassador Imperialis talent. Gains the Xeno Enemy Talent"
    },
    61: {
        "description": "Ignorance is a wisdom of its own.",
        "effect": "Lose 3 Perception. The first time they would gain 1 or more Insanity points each session, they reduce that amount by 1 (to a minimum of 0) instead."
    },
    62: {
        "description": "Your life is not your own to waste.",
        "effect": "Gain the Die Hard talent. If you already have this skill, Gain 2 Willpower."
    },
    63: {
        "description": "The Emperor often protects best those who fight for him the hardest.",
        "effect": "Gain the Devastating Assault talent. If you already have this talent, Gain 2 Weapon Skill."
    },
    64: {
        "description": "The gun is mightier than the sword.",
        "effect": "Gain 3 Ballistic Skill."
    },
    65: {
        "description": "As the mind to the body so the soul to the spirit.",
        "effect": "Gain 3 Toughness OR Gain 3 Intelligence. Lose 3 Agility OR Lose 3 Perception."
    },
    66: {
        "description": "The coin of the forbidden is worth little yet can buy souls uncounted.",
        "effect": "Lose 5 Strength. Lose 5 Intelligence. Gains Minor Mental Disorder - Compulsion 'New Experiences'"
    },
    67: {
        "description": "Do not dream above your allotted station in the Imperial Creed.",
        "effect": "Gain the Intimidation Skill at Rank 1 (Known). If you already have this skill, Gain 2 Willpower."
    },
    68: {
        "description": "Blind faith is a just cause.",
        "effect": "Gain the Blind Fighting talent. If you already have this talent, Gain 2 Willpower OR Gain 2 Perception."
    },
    69: {
        "description": "Promethium is salvation for the wicked: be generous with its merciful touch.",
        "effect": "If this character is using a Flame weapon with an arc, increase the arc of application by an additional 10 degrees."
    },
    70: {
        "description": "Mercy is not for a man, not for a city, not for a nation, not even for a world.",
        "effect": "This character must make a Challenging (+0) Willpower test when in a position to spare an enemy. If they fail then they will act in a manner that dispatches the enemy as expediently (and violently) as possible."
    },
    71: {
        "description": "A suspicious mind is a healthy mind.",
        "effect": "Gain 2 Perception. Additionally, they may re-roll Awareness tests to avoid being Surprised."
    },
    72: {
        "description": "In the darkness, follow the light of Terra.",
        "effect": "Gain 3 Willpower."
    },
    73: {
        "description": "By the purity of our righteous fire shall we cleanse tainted worlds.",
        "effect": "Gain the Two Weapon Wielder talent. If you already have this talent, Gain 2 Weapon Skill OR Gain 2 Ballistic Skill."
    },
    74: {
        "description": "Suffering is an unrelenting instructor.",
        "effect": "Lose 3 Toughness. The first time that this character suffers any damage each session, he gains a +20 bonus to the next test he makes before the end of his next turn."
    },
    75: {
        "description": "Deeds are but the pale ghosts of intentions.",
        "effect": "This character gains the Logic skill at Rank 1 (Known). If they already possess this skill, increase their Intelligence characteristic by 2 instead."
    },
    76: {
        "description": "The only true fear is dying without your duty done.",
        "effect": "Gain the Resistance (Cold, Heat, or Fear) talent. If you already have this talent, Gain 2 Toughness."
    },
    77: {
        "description": "Death spares the innocent from inevitable corruption.",
        "effect": "Lose 5 Agility. Lose 5 Willpower. When attempting to resist Toxins Trait effects increase the test as if the Toxin trait was (X+1)."
    },
    78: {
        "description": "By my fury they shall know the Emperor’s Name.",
        "effect": "Gain the Swift Attack talent. If you already have this talent, Gain 2 Weapon Skill."
    },
    79: {
        "description": "The enemies of Man cannot stand before the Emperor’s chosen.",
        "effect": "Gain the Leap Up talent. If you already have this talent, Gain 2 Agility."
    },
    80: {
        "description": "When the Heretic turns from the Master of Mankind, he turns his back on his very humanity.",
        "effect": "Gain the Peer talent (Herectical). This has left them with a noticeable mark which in certain situations will give a (-10) to social interactions."
    },
    81: {
        "description": "Fear most that which lurketh unseen.",
        "effect": "Gain the Nowhere to Hide talent. If you already have this talent, Gain 2 Perception."
    },
    82: {
        "description": "A weapon’s place is not to question.",
        "effect": "Gain the Ambidextrous talent. If you already have this talent, Gain 2 Agility."
    },
    83: {
        "description": "The Emperor’s deliverance relies upon the guns of the Battlefleet.",
        "effect": "Gain the Marksman talent. If you already have this talent, Gain 2 Ballistic Skill."
    },
    84: {
        "description": "Innocence is an illusion.",
        "effect": "Gain the Keen Intuition talent. If you already have this talent, Gain 2 Intelligence."
    },
    85: {
        "description": "Judge not the righteous, lest you be judged and found wanting.",
        "effect": "Gain the Interrogation skill (Rank 1). If you already have this skill, Gain 2 Strength OR Gain 2 Wilpower."
    },
    86: {
        "description": "All sinners fear the Emperor’s wrath.",
        "effect": "Gain the Frenzy talent. If you already have this talent, Gain 2 Toughness."
    },
    87: {
        "description": "Courage Comes from Duty.",
        "effect": "Gain the Iron Jaw talent. If you already have this skill, Gain 2 Willpower."
    },
    88: {
        "description": "There is no peace among the stars.",
        "effect": "Lose 5 Ballistic Skill. Lose 5 Fellowship. When attempting to Disengage an opponent, this character must pass a Challenging (+0) Willpower test or become Stunned."
    },
    89: {
        "description": "To war is human.",
        "effect": "Gain the Dodge skill (Rank 1). If you already have this skill, Gain 2 Agility."
    },
    90: {
        "description": "Scorn the heretic; his path will end in eternal damnation.",
        "effect": "Gain the Psyniscience skill (Rank 1). Increase this character's Insanity Points by their Intelligence Bonus."
    },
    91: {
        "description": "Our faith hones our hate to be clean and strong.",
        "effect": "Gain the Rapid Reload talent. If you already have this talent, Gain 2 Ballistic Skill."
    },
    92: {
        "description": "There is no substitute for zeal.",
        "effect": "Gain the Clues from the Crowds talent. If you already have this talent, Gain 2 Fellowship."
    },
    93: {
        "description": "In His service one is never sacrificing.",
        "effect": "Gain the Sound Constitution talent. If you already have this talent, Gain 2 Toughness."
    },
    94: {
        "description": "By his assassins will you know his worth.",
        "effect": "Gain the Stealth skill (Rank 1). If you already have this skill, Gain 2 Agility."
    },
    95: {
        "description": "Oppose the Alien at every road, it is your duty.",
        "effect": "Gain the Exotic Weapon Proficiency (Single Weapon) talent."
    },
    96: {
        "description": "Even a man who has nothing can still offer his life.",
        "effect": "Gain 2 Strength."
    },
    97: {
        "description": "Only in death does duty end.",
        "effect": "The first time this character would suffer Fatigue each session, they suffer that amount of Fatigue minus 1 (to a minimum of 0) instead."
    },
    98: {
        "description": "An ocean of courage is not the equal of a drop of faith.",
        "effect": "The first time a session this character spends a Fate Point to gain a bonus to a Fear Test, they gain a further (+10) bonus."
    },
    99: {
        "description": "Know that the warp goes where it pleases.",
        "effect": "Lose 5 Weapon Skill. Lose 5 Toughness. When attempting to resist a Malignancy or Mutation Test, increase the difficulty of the test by one degree."
    },
    100: {
        "description": "Do not ask why you serve. Only ask how.",
        "effect": "Gain 1 Fath Threshold."
    }
}

# Calculating Wounds
def calculate_wounds(base_wounds):
    additional_wounds = random.randint(1, 5)  # Roll 1d5
    total_wounds = base_wounds + additional_wounds
    print(f"Base Wounds: {base_wounds}\nAdditional Wounds (1d5): {additional_wounds}\nTotal Wounds: {total_wounds}")
    return total_wounds

# twist of fate
def roll_twist_of_fate():
    roll = random.randint(1, 100)
    print(f"\nYou rolled a d100 and got: {roll}")

    if roll in twist_of_fate_table:
        outcome = twist_of_fate_table[roll]
        print(f"Your Divination is: {outcome['description']} - Effect: {outcome['effect']}")
        return outcome
    else:
        print("No outcome found for this roll.")
        return "No outcome found for this roll."


        # Character class
class Character:
    def __init__(self, name, homeworld, background, role):
        self.name = name
        self.homeworld = homeworld
        self.background = background
        self.role = role
        self.characteristics = self.roll_characteristics(homeworld)
        self.selected_skills = None
        self.selected_equipment = None
        self.selected_talents = None
        self.selected_aptitudes = None
        self.selected_role_talents = None
        self.selected_role_aptitudes = None
        self.wounds = None

    def roll_characteristics(self, homeworld):
        char_data = homeworlds[homeworld]
        characteristics = {
            "Weapon Skill": self.roll("Weapon Skill", char_data),
            "Ballistic Skill": self.roll("Ballistic Skill", char_data),
            "Strength": self.roll("Strength", char_data),
            "Toughness": self.roll("Toughness", char_data),
            "Agility": self.roll("Agility", char_data),
            "Intelligence": self.roll("Intelligence", char_data),
            "Perception": self.roll("Perception", char_data),
            "Willpower": self.roll("Willpower", char_data),
            "Fellowship": self.roll("Fellowship", char_data),
            "Influence": self.roll("Influence", char_data),
        }
        return characteristics

    def roll(self, characteristic, char_data):
        if characteristic in char_data['advantages']:
            return self.roll_advantage()
        elif characteristic in char_data['disadvantages']:
            return self.roll_disadvantage()
        else:
            return self.roll_standard()

    def roll_standard(self):
        return 20 + random.randint(1, 10) + random.randint(1, 10)

    def roll_advantage(self):
        rolls = [random.randint(1, 10) for _ in range(3)]
        return 20 + sum(rolls) - min(rolls)

    def roll_disadvantage(self):
        rolls = [random.randint(1, 10) for _ in range(3)]
        return 20 + sum(rolls) - max(rolls)

# Function to choose an option with confirmation
def choose_option(options, data_dict):
    while True:
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")

        user_input = input("Choose an option (or type 'EXIT' to close the program): ")
        if user_input.lower() == 'exit':
            print("Exiting program...")
            exit(0)

        try:
            choice = int(user_input)
            if 1 <= choice <= len(options):
                selected_option = options[choice - 1]
                option_data = data_dict[selected_option]

                print(f"\nSelected: {selected_option}")
                for key, value in option_data.items():
                    if isinstance(value, list):
                        value = ', '.join(value)
                    formatted_key = ' '.join(word.capitalize() for word in key.replace('_', ' ').split())
                    print(f"{formatted_key}: {value}")

                confirm = input("Confirm this choice? Y/N: ").strip().lower()
                if confirm == 'y':
                    return selected_option
                else:
                    print("Choose Again, Acolyte.")
            else:
                print("Invalid option. Choose again, profligate.")
        except ValueError:
            print("Enter a number.")


# Function to reroll a characteristic using number selection
def reroll_characteristic(character, homeworld):
    characteristics_list = list(character.characteristics.keys())

    print("\nYou may choose one characteristic to reroll:")
    for index, char in enumerate(characteristics_list, start=1):
        print(f"{index}. {char}: {character.characteristics[char]}")

    while True:
        try:
            choice_index = int(input("Enter the number of the characteristic to reroll, or '0' to skip: "))
            if choice_index == 0:
                break
            if 1 <= choice_index <= len(characteristics_list):
                chosen_char = characteristics_list[choice_index - 1]
                char_data = homeworlds[homeworld]

                if chosen_char in char_data['advantages']:
                    new_roll = character.roll_advantage()
                elif chosen_char in char_data['disadvantages']:
                    new_roll = character.roll_disadvantage()
                else:
                    new_roll = character.roll_standard()

                character.characteristics[chosen_char] = new_roll
                print(f"New {chosen_char}: {new_roll}")
                break
            else:
                print("Invalid number. Enter again, profligate.")
        except ValueError:
            print("Enter a number.")


def select_background_role_options(character, data_backgrounds, data_roles):
    print("\nSelect options for your Background and Role:")

    background_data = data_backgrounds[character.background]
    role_data = data_roles[character.role]

    # Make selections for 'or' separated options
    character.selected_skills = make_selections('starting_skills', background_data, character.background)
    character.selected_equipment = make_selections('starting_equipment', background_data, character.background)
    character.selected_talents = make_selections('starting_talents', background_data, character.background)
    character.selected_aptitudes = make_selections('starting_aptitudes', background_data, character.background)
    character.selected_role_talents = make_selections('Role Talents', role_data, character.role)
    character.selected_role_aptitudes = make_selections('Role Aptitudes', role_data, character.role)

    # ...

def make_selections(category_name, data, entity_name):
    if category_name in data:
        # Split the string into options based on the semicolon delimiter
        options = data[category_name].split(';')
        chosen_options = []

        for option in options:
            # Strip whitespace from the current option
            option = option.strip()

            # Check for 'or' options
            if ' or ' in option:
                print(f"\nChoices for {category_name.replace('_', ' ')} of {entity_name}:")
                # Split on 'or' to create sub-options
                sub_options = [sub_option.strip() for sub_option in re.split(r'\s+or\s+', option)]
                chosen_option = choose_from_options(sub_options)
                chosen_options.append(chosen_option)
                print(f"You have chosen: {chosen_option}")
            else:
                # No 'or', so add the option directly
                chosen_options.append(option)

        return chosen_options


def choose_from_options(options):
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        choice = input("Choose an option: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("Invalid option, please choose a valid number.")

def output_character_to_file(character):
    with open(f"{character.name}_character_sheet.txt", "w") as file:
        file.write(f"Character Name: {character.name}\n")
        file.write(f"Homeworld: {character.homeworld}\n")
        file.write(f"Background: {character.background}\n")
        file.write(f"Role: {character.role}\n\n")

        file.write("Characteristics:\n")
        for key, value in character.characteristics.items():
            display_key = key.replace('_', ' ').title()  # Add this line
            file.write(f"{display_key}: {value}\n")  # Update this line

        file.write("\nSelected Skills:\n")
        file.write(f"{character.selected_skills}\n")

        file.write("\nSelected Equipment:\n")
        file.write(f"{character.selected_equipment}\n")

        file.write("\nSelected Talents:\n")
        file.write(f"{character.selected_talents}\n")

        file.write("\nSelected Aptitudes:\n")
        file.write(f"{character.selected_aptitudes}\n")

        file.write("\nSelected Role Talents:\n")
        file.write(f"{character.selected_role_talents}\n")

        file.write("\nSelected Role Aptitudes:\n")
        file.write(f"{character.selected_role_aptitudes}\n")

        file.write("\nTwist of Fate:\n")
        file.write(f"{character.twist_of_fate}\n")

        # Add any additional information you want to include in the character sheet

        print(f"Character sheet saved as {character.name}_character_sheet.txt")


def main():
    ascii_art="""



IIIIIIIIII
I::::::::I
I::::::::I
II::::::II
  I::::I  
  I::::I  
  I::::I  
  I::::I  
  I::::I  
  I::::I  
  I::::I  
  I::::I  
II::::::II
I::::::::I
I::::::::I
IIIIIIIIII
FOR THE GLORY
  OF THE IMPERIUM



"""
    centered_art = "\n".join(line.center(70) for line in ascii_art.strip().split('\n'))
    print(centered_art)
    print("Welcome, Acolyte. Tell us your history.".center(70))

    # Homeworld selection
    homeworld_options = list(homeworlds.keys())
    print("\nThis was your birthplace among the stars:".center(70))
    homeworld = choose_option(homeworld_options, homeworlds)

    # Background selection
    background_options = list(backgrounds.keys())
    print("\nExplain your Background:".center(70))
    background = choose_option(background_options, backgrounds)

    # Role selection
    role_options = list(roles.keys())
    print("\nDecide your Role:".center(70))
    role = choose_option(role_options, roles)

    name_input = input("\nEnter your name (or type 'EXIT' to close the program): ".center(70))
    if name_input.lower() == 'exit':
        print("Exiting program...".center(70))
        exit(0)

    character = Character(name_input, homeworld, background, role)
    base_wounds = homeworlds[homeworld]['base_wounds']
    character.wounds = calculate_wounds(base_wounds)

    reroll_characteristic(character, homeworld)

    # Display final characteristics after potential reroll
    print("\nFinal Character Details:".center(70))
    for char, value in character.characteristics.items():
        print(f"{char}: {value}".center(70))
    print(f"Wounds: {character.wounds}".center(70))

    # Player selects options for Background and Role
    select_background_role_options(character, backgrounds, roles)

    # Roll for Twist of Fate
    character.twist_of_fate = roll_twist_of_fate()

    output_character_to_file(character)

    # TODO: Implement additional character creation steps


if __name__ == "__main__":
    main()
