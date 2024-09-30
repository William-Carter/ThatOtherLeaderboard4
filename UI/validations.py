def checkDateFormat(dateString: str) -> bool:
    if dateString.count("-") != 2:
        return False
    
    splitString = dateString.split("-")
    if len(splitString) != 3:
        return False
    
    for part in splitString:
        if not part.isdigit():
            return False
        
    if len(splitString[0]) != 4:
        return False
        
    if int(splitString[1]) > 12:
        return False
    
    if int(splitString[2]) > 31:
        return False
        

    return True
        

    

if __name__ == "__main__":
    print(checkDateFormat(""))
    



