class openapepose_to_dlc:
    import json
    import pandas as pd 
    import numpy as np

    def __init__(path, experimenter, species, destination):
        """
        input variables: 
        path = path to your annotation file (str)
        experimenter = name of experimenter as used in DLC (str)
        species = list of species (strings) you want to include, if you want all species use: ['Chimpanzee', 'Bonobo', 'Gorilla', 'Siamang', 'Orangutan', 'Gibbon']
        destination = path where you want output file stored including output file name without extension, example: 'user/dlc/openapepose_data'

        outputs: 
        .h5 file in deeplabcut format of the json-annotation file 
        """
        self.path = path
        self.experimenter = experimenter
        self.species = species
        self.keypoints = ['bodyparts', 'Nose', 'Left_Eye', 'Right_Eye', 'Head', 'Neck', 'Left_Shoulder', 'Left_Elbow', 'Left_Wrist', 'Right_Shoulder', 'Right_Elbow', 'Right_Wrist', 'Hip/Sacrum', 'Left_Knee', 'Left_Foot', 'Right_Knee', 'Right_Foot']
        self.destination = destination

    
    def load_file(self):
    
    # load data using Python JSON module
        with open(self.path,'r') as f:
            data = json.loads(f.read())
            openape_df = pd.json_normalize(data, record_path =['data'])
        return openape_df
    
    def extract_keypoints(self):
        keypoints = self.keypoints
        keypoints = [val for val in keypoints for _ in (0, 1)] #create a list where all keypoints are double represented so we can store x and y coordinates 
        keypoints.pop(0) #delete duplicate 'bodyparts'
        return keypoints
    
    def extract_coords(self, keypoints = extract_keypoints()):
        coords = ['coords'] #create the coordinates columns
        stoppoint = (len(keypoints)-1)/2 

        #create list with alternating x and y column names
        for i in range(0,int(stoppoint)): 
            coords.append('x')
            coords.append('y')
        
        return coords



    def extract_experimenter(self, coords = extract_coords()):
        #create list with experimentername
        scorer = self.experimenter
        experimenter_list = ['scorer']
        for i in range(0,len(coords)-1):
            experimenter_list.append(scorer+str(i))

        return experimenter_list
    
    def create_dataframe(self, openape_df = load_file(), keypoints = extract_keypoints(), coords = extract_coords(), experimenter_list = extract_experimenter()):
        openape_df_species = openape_df[openape_df['species'].isin(self.species)]
        
        #get landmarks out of the open ape annotation file 
        landmarks_dlc = openape_df_species['landmarks'].values.tolist()

        #get filenames out of the openape annotation file
        filenameslist = [[filename] for filename in list(openape_df_species['file'])]

        filename_landmarks = [filenameslist[i]+landmarks_dlc[i] for i in range(len(filenameslist))]
        
        oap_to_dlc = pd.DataFrame(filename_landmarks,  colums = experimenter_list)
        oap_to_dlc[0] = keypoints
        oap_to_dlc.iloc[1] = coords
        return oap_to_dlc
    
    def save_to_h5(self, oap_to_dlc = create_dataframe()):

        oap_to_dlc.to_hdf(self.destination + '.h5', 'df_with_missing')










