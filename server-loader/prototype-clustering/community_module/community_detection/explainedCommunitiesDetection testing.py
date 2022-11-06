        
        
        # Testing
        
        print("interaction is explainable")
        print(self.data[['emotionsDominantInteractionGenerated']])
        print("\n\n\n")
        
        print("len data: " + str(len(self.data.index)))
        print("len dominant attribute array: " + str(len(self.data['emotionsDominantInteractionGenerated'][0])))
        print("\n\n\n")
        
        print("community: ")
        print(len(community.index))
        print("\n\n\n")
        
        print("data index: " + str(self.data.index))
        print("community index: " + str(community.index))
        print("\n\n\n")
        
        
        print("community_dominantAttributeList")
        print(community_dominantAttributeList)
        print("len dominant attribute array: " + str(len(self.data['emotionsDominantInteractionGenerated'][0])))
        print("len dominant attribute array: " + str(len(df['community_emotionsDominantInteractionGenerated'])))
        print("\n\n\n")
        
        
        print("df")
        print(df)
        print("\n\n\n")
        
        # Check one element
        print("one list")
        print(df['community_emotionsDominantInteractionGenerated'])
        print(df['community_emotionsDominantInteractionGenerated2'])
        
        
        print("end")
        print("\n\n\n")