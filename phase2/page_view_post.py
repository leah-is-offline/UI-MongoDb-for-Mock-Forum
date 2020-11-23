from state_machine import State
import db
from util import inputInt

class ViewPost(State):
    # static variable
    postId = None
    def run(self):
        from page_menu import Menu
        from page_make_post import PostAnswer

        global postId
        if (ViewPost.postId == None):
            print('postId must be staticly defined to use this class!')
            return None

        print("-- Viewing post: %s --" % ViewPost.postId )

        post = db.getPost(ViewPost.postId)

        if (post == None):
            print("No such post in databse")
        else:
            for key, value in post.items():
                print('{:15} {}'.format(key+':', value))

            db.updateViewCount(ViewPost.postId)
            

        print("\n\nWhat would you like to do?")

        # Compose the list of user option / actions
        options = [
            ("Vote on post", "func", self.voteOnPost),
            ("Back to Menu", Menu)
        ]

        if post['PostTypeId'] == "1":
            PostAnswer.questionId = ViewPost.postId
            options[-1:-1] = [
                ("List answers", "func", self.showAnswers),
                ("Add an answer", PostAnswer)
            ]

        # Print the available options
        for i, option in enumerate(options, start=1):
            print(str(i)+ ". " + option[0] )
        print()

        # get user input
        choice = inputInt("Please select an option: ")
        while(choice < 1 or choice > len(options)):
            choice = inputInt("Not in range: ")

        # execute func or go to next state
        option = options[choice-1]
        if (option[1] == "func"):
            return option[2]()
        return option[1]

    def voteOnPost(self):
        db.insertVote(ViewPost.postId, "2")
        print("\nSweet! You voted on this post!")
        input("Press enter to continue")
        return ViewPost

    def showAnswers(self):
        pass
        #get list of posts where ParentID = postid
