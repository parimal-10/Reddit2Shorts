import createPost, getConfig
import time

def main():
    startTime = time.time()
    id = createPost.createVideo()
    if(id == None):
        return main()
    endTime = time.time()
    print(f"Total Time: {endTime - startTime}")

if __name__=="__main__":
    main()