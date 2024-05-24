import java.util.Scanner;

class PasswordManager {
	/**
	 */

	private static String USERNAME = "joebob";
	private static String PASSWORD = "PassWord123";

	public static void main(String[] args) {
		passwordManager();
	}

	public static boolean validateUserNameAndPassword(String username, String password) {
		return username.equals(USERNAME) && password.equals(PASSWORD);
	}

	public static void passwordManager() {
		boolean hasValidCredentials = true;
		Scanner scanner = new Scanner(System.in);

		while (hasValidCredentials) {
			System.out.println("Enter user name: ");
			String inputUserName = scanner.nextLine();
			System.out.println("Enter password: ");
			String inputUserPassword = scanner.nextLine();

			if (validateUserNameAndPassword(inputUserName, inputUserPassword)) {
				System.out.println("Credentials accepted!\n");
				System.out.println("Secret is: You got this :) \n");
				scanner.close();
				hasValidCredentials = false;
			} else {
				System.out.println("Invalid username or password. Please try again:");
			}
			
		}
	}
}