from openai import OpenAI

# load gpt key
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GPT_TOKEN')


CONVERSATIONS_DIRECTORY = 'conversations'


class GPTclient:
    def __init__(self):
        self.selected_conv_name = None
        self.history = None
        self.conv_file_names = None

    def load_conversation_names(self):
        self.conv_file_names = [f for f in os.listdir('conversations') if os.path.isfile(os.path.join('conversations', f))]
        if len(self.conv_file_names) == 0:
            print('No conversations to select from.')
        else:
            print('Available conversations:')
            counter = 1
            for conv_file_name in self.conv_file_names:
                print(f'{counter} - {conv_file_name[:-4]}')
                counter += 1
    
    def run(self):
        while True:
            try:
                self.load_history()
                if self.history is None:
                    return
                self.do_conversation()
            except:
                continue

    def load_history(self):
        
        print()
        print('Welcome to the Bojodojo GPT client!')
        print()
        print('Possible commands:')
        print('CONTINUE [n] - continue conversation with given index (e.g. \'CONTINUE 3\')')
        print('NEW [title] - start new conversation with given name (e.g. \'NEW Pet name ideas\')')
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
                    raise Exception('Missing index or title')

                if command == 'CONTINUE':
                    if not substance.isdigit():
                        raise Exception('Conversation index not integer')
                    if int(substance) > len(self.conv_file_names):
                        raise Exception('Conversation index out of range')
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
                        raise Exception('Conversation index not integer')
                    if int(substance) > len(self.conv_file_names):
                        raise Exception('Conversation index out of range')
                    conv_name_to_remove = self.conv_file_names[int(substance) - 1]
                    os.remove(f'{CONVERSATIONS_DIRECTORY}\\{conv_name_to_remove}')
                    self.load_conversation_names()
                    print()
                    continue

                else:
                    raise Exception('Command does not exist')

            except Exception as e:
                print(f'Invalid command ({e}), try again.')
                print()
                pass

    
    def do_conversation(self):

        self.client = OpenAI(api_key=key)

        if len(self.history) > 0:
            user_input = input('Print conversation history? (y/N)? ')
            print()
            if user_input.lower() in ['y', 'yes']:
                print(self.history)

        while True:

            context = f'You are a helper bot, continuing a conversation. Here is the existing history:\n\n{self.history}End of history. Try to make your answers relatively short.'

            user_input = input('Ask a question or write STOP to go back to the menu:\n\n')
            print()

            if user_input == 'STOP':
                self.history = None
                raise Exception

            completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_input}
            ]
            )

            bot_answer = completion.choices[0].message.content
            print(bot_answer)
            print()

            self.history += f'USER INPUT: {user_input}\n\nBOT REPLY: {bot_answer}\n\n'

            with open(f'{CONVERSATIONS_DIRECTORY}\\{self.selected_conv_name}.txt', 'w') as f:
                f.write(self.history)



if __name__ == "__main__":
    GPTclient().run()