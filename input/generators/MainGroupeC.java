package instances;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Main {
    
    // method to create a file with just a given name
    public static File createFile(String fileName) {
        try {
            File file = new File(fileName);
            FileWriter writer = new FileWriter(file);
            Random rand = new Random();
            int R =(rand.nextInt(10000) + 1);
            int C = (rand.nextInt(10000) + 1) ;
            int F =  (rand.nextInt(1000) + 1);
            int N= (rand.nextInt(10000) + 1);
            int B = (rand.nextInt(10000) + 1);
            int T = (rand.nextInt(1000000000) + 1);           
            String firstLine = R + " " +
                              C + " " +
                              F + " " +
                              N + " " +
                              B + " " +
                              T;

            writer.write(firstLine);
            writer.write("\n");
            
            // Generate exactly N rides
            for (int i = 0; i < N; i++) {
                int a, b, x, y, s, f;
                boolean validRide = false;
                
                
                do {
                    a = rand.nextInt(R);
                    b = rand.nextInt(C);
                    x = rand.nextInt(R);
                    y = rand.nextInt(C);
                    s = rand.nextInt(T);
                    f = rand.nextInt(T + 1); 
                    
                    // Check constraints:
                   
                    if ((a != x || b != y) && f >= s + Math.abs(x - a) + Math.abs(y - b)) {
                        validRide = true;
                    }
                } while (!validRide);
                
                String line = a + " " +
                              b + " " +
                              x + " " +
                              y + " " +
                              s + " " +
                              f + "\n";
                writer.write(line);
            }            
            writer.close();
            return file;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
    public static void main(String[] args) {
        // Example usage
        createFile("output.txt");
        
    }
}
