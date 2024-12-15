import json

def get_characters(file_path):
    with open(file_path,'r') as f:
        file = json.load(f)
    
    character = 0    
    for i in range(len(file)):
        character = character + len(file[i]['content'].split(' '))
    
    return character/len(file)

print(get_characters('/shared/nas/data/m1/jiateng5/Semafor_Additional_Exp/final_data/cleaned_final_data/Polifact.json'))
print(get_characters('/shared/nas/data/m1/jiateng5/Semafor_Additional_Exp/final_data/cleaned_final_data/ptc_human_annotated.json'))
print(get_characters('/shared/nas/data/m1/jiateng5/Semafor_Additional_Exp/final_data/cleaned_final_data/RUWA.json'))
        