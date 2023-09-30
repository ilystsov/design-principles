import sys
import requests
from abc import ABC, abstractmethod


class IOHandler(ABC):
    """This class implements input and output logic to interact with the player."""
    @abstractmethod
    def write(self, text: str) -> None:
        """
        Abstract method for writing text.

        :param text: str
        """
        pass

    @abstractmethod
    def read(self) -> str:
        """
        Abstract method for reading text.

        :return: str
        """
        pass


class IOConsole(IOHandler):
    """This class implements input and output console interface."""
    def write(self, text: str) -> None:
        """
        Write the given text to console standard output stream.

        :param text: str
        """
        sys.stdout.write(text)
        sys.stdout.flush()

    def read(self) -> str:
        """
        Read char and linefeed from the console standard input stream and delete linefeed.

        :return: char
        """
        char = sys.stdin.read(2).rstrip('\n')
        return char


class ChooseWord(ABC):
    """This class implements generating random word logic."""
    @abstractmethod
    def choose_word(self) -> str:
        """
        Abstract method for returning random word.

        :return: str
        """
        pass


class ChooseWordFromAPI(ChooseWord):
    """This class implements generating random word with API."""
    def __init__(self, io_handler: IOHandler) -> None:
        """
        Initialize output logic to write error messages.

        :param io_handler: IOHandler
        """
        self.io_handler = io_handler

    def choose_word(self) -> str:
        """
        Return a random word from API.

        >>> ChooseWordFromAPI().choose_word()
        apple

        :return: str
        """
        timeout = 10
        try:
            response = requests.get('https://random-word-api.herokuapp.com/word', timeout=timeout)
        except requests.exceptions.Timeout:
            self.io_handler.write('Server did not respond in {timeout} seconds. We are sorry :(\n'.format(timeout=timeout))
            sys.exit(1)
        except requests.exceptions.RequestException as error:
            self.io_handler.write('An error occurred: {error}. We are sorry :(\n'.format(error=error))
            sys.exit(1)
        return response.text[2:-2]


class HangmanGame(object):
    """
    This class implements Hangman game.

    Attributes:
    word: the word to guess
    word_chars: a set of unique letters that make up a word
    guessed_chars: a set of chars, guessed by a player
    attempted_chars: a set of chars, proposed by a player
    guesses_cnt: a number of attempts
    """

    def __init__(self, choose_word_method: ChooseWord, io_handler: IOHandler) -> None:
        """
        Initialize HangmanGame class instance.

        :param choose_word_method: ChooseWord
        :param io_handler: IOHandler
        """
        self.io_handler = io_handler
        self.word: str = choose_word_method.choose_word()
        self.word_chars: set[str] = set(self.word)
        self.guessed_chars: set[str] = set()
        self.attempted_chars: set[str] = set()
        self.guesses_cnt: int = len(self.word)

    def make_hidden_word(self) -> str:
        """
        Get a word representation with underlines for player.

        >>> HangmanGame().make_hidden_word()
        app_e

        :return: str
        """
        hidden_word: str = ''
        blank: str = '_'
        for char in self.word:
            if char in self.guessed_chars:
                hidden_word += char
            else:
                hidden_word += blank
        return hidden_word

    def game_end(self) -> bool:
        """
        Check if the game is over.

        :return: bool
        """
        guessed_chars_len: int = len(self.guessed_chars)
        word_chars_len: int = len(self.word_chars)
        return self.guesses_cnt == 0 or guessed_chars_len == word_chars_len

    def wrong_char(self, char: str) -> None:
        """
        Actions if the char proposed is incorrect.

        :param char: char
        """
        self.attempted_chars.add(char)
        self.guesses_cnt -= 1
        if self.guesses_cnt != 0:
            self.io_handler.write('Wrong\nYou have {number} more guesses\n'.format(number=self.guesses_cnt))

    def right_char(self, char: str) -> None:
        """
        Actions if the char proposed is correct.

        :param char: char
        """
        self.attempted_chars.add(char)
        self.guessed_chars.add(char)

    def play(self) -> None:
        """Proceed the player's input, show the player's progress. Output the result of the game."""
        self.io_handler.write('Start guessing...\n')
        while not self.game_end():
            self.io_handler.write('{word} guess a character: '.format(word=self.make_hidden_word()))
            char: str = self.io_handler.read().lower()
            if char in self.attempted_chars:
                self.io_handler.write("You've already tried character '{char}'. Try another one\n".format(char=char))
            else:
                if char not in self.word_chars:
                    self.wrong_char(char)
                else:
                    self.right_char(char)
        if self.guesses_cnt == 0:
            self.io_handler.write('You lose. The word is {word}\n'.format(word=self.word))
        else:
            self.io_handler.write('{word} You win\n'.format(word=self.word))


if __name__ == '__main__':
    io_handler = IOConsole()
    choose_word_method = ChooseWordFromAPI(io_handler)
    HangmanGame(choose_word_method, io_handler).play()
