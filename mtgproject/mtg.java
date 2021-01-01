import java.io.BufferedReader;
import java.util.HashMap;
import java.util.Scanner;
public class MTG{
    public static void main(String [] args){
        Scanner console = new Scanner(system.in);
        System.out.print("Enter a sequence: ");
        String test = isValid(console);
        System.out.println(test);

        fillmap();
    }

    public static String isValid(Scanner console){
        
        String valid = console.nextLine();
        while(valid.length() !=0)
        {
         System.out.print("Enter a valid string: ");
         while(valid.length() <= 5)
         {
            console.nextLine();
            System.out.print("Enter a valid string: ");
         }
         valid = console.nextLine();
      }
        return valid;
    }
    /*public static char isAnagram(String valid){

    }*/

    private static void fillMap(){
        //file path for buffer reader
        String filePath = "keys.txt";
        //hashmap to fill
        HashMap<String, String> map = new HashMap<>();
        File file = new File(filePath);
        //creates a BufferedReader object to read the file
        try{
            buff = new BufferedReader(new FileReader(file));
            String line = null;

            while((line = buff.readLine()) != null){
                String[] parts = line.split(":");
                String key = parts[0].trim();
                String value = parts[1].trim();
                if(!key.equals("") && !value.equals("")){
                    map.put(key,value);
                }

            }

        }catch(Exception e){
            e.printStackTrace();
        }finally{
            if(buff != null){
                buff.close();  
        }
        
    }
}
}
