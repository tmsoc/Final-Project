from restDataAccess import Model
from controller import Controller


def main():
    model = Model()
    controller = Controller(model)

    model.close_connection()


if __name__ == "__main__":
    main()
