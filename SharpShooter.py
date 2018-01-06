import random
import sys
import os

Level_Proficiency_List              = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]
Sneak_Attack_Number_Of_Dice_List    = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]

#######################################################################################################################
# START OF ENTERING YOUR INFO

FileName = 'RogueFighter.csv'
OtherHitModifier = 1 # +1 Magic Weapon
OtherHitModifier = OtherHitModifier + 2 # ArcheryMastery = +2
OtherDamageModifier = 1 # +1 Magic weapon
DexModifier = 3 # Dexterity Modifier
CharacterLevel = 5 # Total Character Level, used to determine proficiency bonus

#If you are not a rogue set this value to 0
RogueLevel = 4 # Used to determine number of sneak attack dice used

# Change for specific weapon you are using
# Hand Crossbow = 1d6
NumberOfWeaponDice = 1
SidesOnWeaponDice = 6

# Sneak Attack
# Level 4 Rogue Sneak Attack is 2d6
NumberOfSneakAttackDice = Sneak_Attack_Number_Of_Dice_List[RogueLevel]
SidesOnSneakAttackDice = 6

# Choose the armor class range you want to get info for
ArmorClassMin = 10
ArmorClassMax = 30

# END OF ENTERING YOUR INFO
#######################################################################################################################

# Normal chance to hit for ranged includes dex modifier, proficiency and any extra modifier such as Fighter Archery Style
NormalHitModifier = DexModifier + Level_Proficiency_List[CharacterLevel - 1] + OtherHitModifier

# AFAIK SharpShooter Hit Modifier will always be the same as normal but -5
SharpShooterHitModifier = NormalHitModifier - 5

# The Average Damage for a single die will be ((#OfSides + 1)/2)
# For Sneak Attack all the dice have the same number of sides so we multiply by the number of dice for your current rogue level
AverageSneakAttackDamage = ((SidesOnSneakAttackDice + 1) / 2) * NumberOfSneakAttackDice

# Since sneak attack is damage is only made up of dice we can multiple the average normal damage by 2 to get average crit damage
AverageSneakAttackCritDamage = AverageSneakAttackDamage * 2
#print('AverageSneakAttackDamage = %s' % AverageSneakAttackDamage)
#print('AverageSneakAttackCritDamage = %s' % AverageSneakAttackCritDamage)

# Ranged Weapon Damage uses the dice roll + Dexterity Modifier for damage, also add on any extra damage such as magic weapon +1
# The Average Damage for a single die will be ((#OfSides + 1)/2)
AverageNormalDamage = (((SidesOnWeaponDice + 1)/2)*NumberOfWeaponDice) + DexModifier + OtherDamageModifier

# Since we use the Dex modifier (And any other modifier like magic weapon +1) for damage on ranged attacks we can't just multiply the normal avg dmg by 2
# Instead we do not divide by 2 after adding 1 to the #OfSides on the die
AverageNormalCritDamage = ((SidesOnWeaponDice + 1)*NumberOfWeaponDice) + DexModifier + OtherDamageModifier
#print('AverageNormalDamage = %s' % AverageNormalDamage)
#print('AverageNormalCritDamage = %s' % AverageNormalCritDamage)

# For sharpshooter we add 10 as extra damage
AverageSharpShooterDamage = AverageNormalDamage + 10
AverageSharpShooterCritDamage = AverageNormalCritDamage + 10
#print('AverageSharpShooterDamage = %s' % AverageSharpShooterDamage)
#print('AverageSharpShooterCritDamage = %s' % AverageSharpShooterCritDamage)

#######################################################################################################################

# Ask for forgiveness not permission, try to remove the file and if it doesn't exist then ignore the error and continue
try:
    os.remove(FileName)
except OSError:
    pass

# I am not smart enough to auto make graphs and shiznit so I just output the results as a CSV file and open it in Excel
# From there I can make the Graphs fairly easily
CsvFile = open(FileName,"w+")

# Mornal (0), Advantage(1) and Disadvantage(2)
Normal = 0
Advantage = 1
Disadvantage = 2

# Loop through twice, 0 is for 'Not Sneak Attack' and 1 is for 'Sneak Attack'
for IsSneakAttack in range (0, 2) :

    # Calculate Mornal (0), Advantage(1) and Disadvantage(2) in one loop
    # Python 'For' Loops go from Start to End - 1 so we have to add 1 to get the correct range
    for AttackType in range(Normal, Disadvantage + 1) :

        # Write appropriate attack type to csv file
        if (AttackType == Normal) :
            if IsSneakAttack :
                CsvFile.write('\nNormal Attack with Sneak Attack\n')
            else:
                CsvFile.write('\nNormal Attack\n')
        elif (AttackType == Advantage) :
            if IsSneakAttack :
                CsvFile.write('\nAdvantage Attack with Sneak Attack\n')
            else:
                CsvFile.write('\nAdvantage Attack\n')
        else:
            if IsSneakAttack :
                CsvFile.write('\nDisadvantage Attack with Sneak Attack\n')
            else:
                CsvFile.write('\nDisadvantage Attack\n')

        CsvFile.write('Armor Class, Normal Hit Chance, Average Normal Damage Per Shot, SS Hit Chance, Average Sharp Shooter Damage Per shot\n')

        # Loop from ArmorClassMin to ArmorClassMax
        # Again, Python 'For' Loops go from Start to target - 1 so we have to add 1 to get the correct range
        for ArmorClass in range(ArmorClassMin, ArmorClassMax + 1) :

            # For each iteration we need to initialize the Number of counted hits to 0
            NumberOfNormalHits = 0
            NumberOfSharpShooterHits = 0

            # For each iteration we need to initialize the Total Damage to 0
            TotalNormalDamage = 0
            TotalSharpShooterDamage = 0

            # Loop through each value of your first D20
            for FirstRoll in range(1, 21) :

                # For a normal attack there is no second roll so change the end value of the next loop to 2 so it only runs once
                # For Advantage or Disadvantage we set the value to 21 so we can go through each outcome of a D20 for the second roll
                if (AttackType == Normal) :
                    SecondRollEnd = 2
                else:
                    SecondRollEnd = 21

                # Loop through each value of your Second D20 (Will make 1 pass if AttackType is Normal)
                for SecondRoll in range(1, SecondRollEnd) :

                    # For a Normal Attack we only Roll 1d20
                    # For Advantage we roll 2d20 and take the larger value
                    # For Disadvantage we roll 2d20 and take the smaller value
                    if (AttackType == Normal) :
                        AttackValue = FirstRoll
                    elif (AttackType == Advantage) :
                        AttackValue = max(FirstRoll, SecondRoll)
                    else :
                        AttackValue = min(FirstRoll, SecondRoll)

                    # If we roll a 20 then it is an automatic hit and we apply crit damage
                    if (AttackValue == 20) :

                        # Increase the number of normal and sharpshooter hits by 1
                        NumberOfNormalHits = NumberOfNormalHits + 1
                        NumberOfSharpShooterHits = NumberOfSharpShooterHits + 1

                        # Increase the total damage of normal and sharpshooter hits by its respective value for average crit damage
                        TotalNormalDamage = TotalNormalDamage + AverageNormalCritDamage
                        TotalSharpShooterDamage = TotalSharpShooterDamage + AverageSharpShooterCritDamage

                        # If this is a Sneak Attack then apply the appropriate average sneak attack crit damage to the normal and sharpshooter total damage
                        if IsSneakAttack :
                            TotalNormalDamage =  TotalNormalDamage + AverageSneakAttackCritDamage
                            TotalSharpShooterDamage = TotalSharpShooterDamage + AverageSneakAttackCritDamage

                    # If we roll a 1 then it is an automatic miss and we do nothing
                    # If it is not a 1 then we calculate if we hit based on targets armor class
                    elif (AttackValue != 1) :

                        # If the current roll + Normal Attack Hit Modifier is greater than or equal to the target armor class then it is a hit
                        if ((AttackValue + NormalHitModifier) >= ArmorClass) :

                            # Increase the number of normal hits by 1
                            NumberOfNormalHits = NumberOfNormalHits + 1

                            # Increase total damage by the average normal damage
                            TotalNormalDamage = TotalNormalDamage + AverageNormalDamage

                            # If this is a Sneak Attack then apply the average sneak attack damage to the normal total damage
                            if IsSneakAttack :
                                TotalNormalDamage = TotalNormalDamage + AverageSneakAttackDamage

                        # If the current roll + SharpShooter Attack Hit Modifier is greater than or equal to the target armor class then it is a hit
                        if ((AttackValue + SharpShooterHitModifier) >= ArmorClass) :

                            # Increase the number of SharpShooter hits by 1
                            NumberOfSharpShooterHits = NumberOfSharpShooterHits + 1

                            # Increase total damage by the average SharpShooter damage
                            TotalSharpShooterDamage = TotalSharpShooterDamage + AverageSharpShooterDamage

                            # If this is a Sneak Attack then apply the average sneak attack damage to the SharpShooter total damage
                            if IsSneakAttack :
                                TotalSharpShooterDamage = TotalSharpShooterDamage + AverageSneakAttackDamage

            # Calculate Hit Percentage by multiplying the number of recorded hits by 100 and dividing by the total number of attempts which is 20 for a normal attack and 400 for advantage or disadvantage
            NormalHitChance = (NumberOfNormalHits * 100) / (FirstRoll * SecondRoll)
            SharpShooterHitChance = (NumberOfSharpShooterHits * 100) / (FirstRoll * SecondRoll)

            # Calculate Average Damage Per Attack/Attempt/Shot by multiplying the Average Damage Per Hit by Chance to Hit
            AverageNormalDamagePerAttack = (NormalHitChance / 100) * (TotalNormalDamage / NumberOfNormalHits)
            AverageSharpShooterDamagePerAttack = (SharpShooterHitChance / 100) * (TotalSharpShooterDamage / NumberOfSharpShooterHits)

            # print('%d, %.2f%%, %.2f, %.2f%%, %.2f\n' % (ArmorClass, NormalHitChance, AverageNormalDamagePerAttack, SharpShooterHitChance, AverageSharpShooterDamagePerAttack))
            CsvFile.write('%d, %.2f%%, %.2f, %.2f%%, %.2f\n' % (ArmorClass, NormalHitChance, AverageNormalDamagePerAttack, SharpShooterHitChance, AverageSharpShooterDamagePerAttack))

    # If we are not a rogue then we don't care about sneak attack scenario
    if (RogueLevel == 0) :
        break

#Close the file since we are done now
CsvFile.close()
