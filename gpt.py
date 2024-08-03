from openai import OpenAI

# load gpt key
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GPT_TOKEN')


CONVERSATIONS_DIRECTORY = 'conversations'

class UserInputError(Exception):
    def __init__(self, message):
        self.message = message

class UserExit(Exception):
    pass

class GPTclient:
    def __init__(self):
        self.selected_conv_name = None
        self.history = None
        self.conv_file_names = None

        self.client = OpenAI(api_key=key)

    def load_conversation_names(self):
        self.conv_file_names = [f for f in os.listdir('conversations') if os.path.isfile(os.path.join('conversations', f))]
        if len(self.conv_file_names) <= 1:
            print('No conversations to select from, start a new one!')
        else:
            print('Available conversations:')
            counter = 1
            for conv_file_name in self.conv_file_names:
                if conv_file_name != 'dummy.txt':
                    print(f'{counter} - {conv_file_name[:-4]}')
                    counter += 1
    
    def test_token(self):
        self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 'test'},
                {"role": "user", "content": 'test'}
            ]
            )

    def run(self):
        try:
            self.test_token()
        except Exception as e:
            print(e)
            return

        while True:
            self.select_conversation_menu()
            if self.history is None:
                return
            
            try:
                self.do_conversation()
            except UserExit:
                continue

    def select_conversation_menu(self):
        
        print()
        print('Welcome to the Bojodojo GPT client!')
        print()
        print('Possible commands:')
        print('NEW [title] - start new conversation with given name (e.g. \'NEW Pet name ideas\')')
        print('CONTINUE [n] - continue conversation with given index (e.g. \'CONTINUE 3\')')
        print('DELETE [n] - delete conversation with given index (e.g. \'DELETE 2\')')
        print('STOP - to exit program')
        print()
        self.load_conversation_names()
        print()

        while True:
            try:
                user_input = input('Input command: ')
                print()
                command = user_input.split(' ')[0]
                substance = ' '.join(user_input.split(' ')[1:])

                if command == 'STOP':
                    print('Stopping...')
                    return
 
                if len(substance) == 0:
                    raise UserInputError('Missing index or title')

                if command == 'CONTINUE':
                    if not substance.isdigit():
                        raise UserInputError('Conversation index not integer')
                    if int(substance) > len(self.conv_file_names):
                        raise UserInputError('Conversation index out of range')
                    conv_file_name = self.conv_file_names[int(substance) - 1]
                    with open(f'{CONVERSATIONS_DIRECTORY}\\{conv_file_name}') as f:
                        self.history = f.read()
                    self.selected_conv_name = conv_file_name[:-4]
                    return

                elif command == 'NEW':
                    with open(f'{CONVERSATIONS_DIRECTORY}\\{substance}.txt', 'w') as _:
                        pass
                    self.selected_conv_name = substance
                    self.history = ''
                    return

                elif command == 'DELETE':
                    if not substance.isdigit():

                        # remove all conversations
                        if substance == 'ALL':
                            for conv_name in self.conv_file_names:
                                if conv_name != 'dummy.txt':
                                    os.remove(f'{CONVERSATIONS_DIRECTORY}\\{conv_name}')
                            self.load_conversation_names()
                            print()
                            continue

                        else:
                            raise UserInputError('Conversation index not integer')
                    if int(substance) > len(self.conv_file_names):
                        raise UserInputError('Conversation index out of range')
                    conv_name_to_remove = self.conv_file_names[int(substance) - 1]
                    os.remove(f'{CONVERSATIONS_DIRECTORY}\\{conv_name_to_remove}')
                    self.load_conversation_names()
                    print()
                    continue

                else:
                    raise UserInputError('Command does not exist')

            except UserInputError as e:
                print(f'Invalid command ({e}), try again.')
                print()

    
    def do_conversation(self):

        if len(self.history) > 0:
            user_input = input('Print conversation history? (y/N)? ')
            print()
            if user_input.lower() in ['y', 'yes']:
                print(self.history, end='')

        print('Ask a question, or type LOAD to load it from input file, or write STOP to go back to the menu:\n')

        while True:

            context = f'You are a helper bot, continuing a conversation. Here is the existing history:\n\n{self.history}End of history. Try to make your answers relatively short.'

            print('USER INPUT: ', end='')
            user_input = input()
            print()

            if user_input == 'STOP':
                self.history = None
                raise UserExit()
            
            if user_input == 'LOAD':
                with open(f'input\\input.txt') as f:
                    user_input = f.read()

            completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_input}
            ]
            )

            bot_answer = '\033[94m' + 'BOT REPLY: ' + completion.choices[0].message.content + '\033[0m'
            print(bot_answer)
            print()

            self.history += f'USER INPUT: {user_input}\n\n{bot_answer}\n\n'

            with open(f'{CONVERSATIONS_DIRECTORY}\\{self.selected_conv_name}.txt', 'w') as f:
                f.write(self.history)



if __name__ == "__main__":
    GPTclient().run()