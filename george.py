import random

def SpongeBobText(input):

	#initialize spongetext variable
	spongetext = ""

	for char in input:
		
		#check if the character is in the alphabet
		if char.isalpha():
			
			random_num = random.random()
			
			#change the character to a capital letter
			if random_num > 0.5:
				
				spongetext += char.upper()
			
			#change the character to a lowercase letter
			else:

				spongetext += char.lower()
		
		#if the character is not in the alphabet, add it to the output without changing
		else:
			
			spongetext += char

	return spongetext

if __name__=="__main__": 
    input_text1 = "Hi! My name is George. Spongebob is my favorite show."
    input_text2 = "Hehe I really hope this works."
    print(SpongeBobText(input_text1)) 
    print(SpongeBobText(input_text2))

