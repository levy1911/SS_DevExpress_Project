/*
 * Connects to SU db and deliveres dependencies information
 */
package suagent;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSetMetaData;

/**
 *
 * @author pawelle
 * @version 0.1
 */



public class SUAgent {
    
    
    // jdbc Connection
    private static String dbURL = "jdbc:derby://scclis:1527/softupdate;user=upd;password=sccupd27245";
    private static Connection conn = null;
    private static Statement stmt = null;
    private static String query = "select e.name as env_name, a.name as apl_name, a.version as apl_ver, da.name as dep_name, da.version as dep_ver\n" +
                                  "from environments e, ocd_apps a, ocd_dependencies d, ocd_apps da\n" +
                                  "where e.name in ('Q409','Q44','Q356') and a.env_id_fk = e.env_id_pk and d.ocd_id_fk = a.ocd_id_pk and da.env_related_id = d.env_related_id\n" +
                                  "order by e.name, a.name, a.version, da.name, da.version";
    private static String query_env = "select distinct(environments.name) from environments";
    
    public static void main(String[] args) {
        // TODO code application logic here
        setConnection();
        selectAll();
        
    }
    
    private static void setConnection() {   
        try {    
            Class derbyClass = Class.forName("org.apache.derby.jdbc.ClientDriver");      
            
            if (derbyClass != null) {                
                derbyClass.newInstance();
            } 
                
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        try {    
           conn = DriverManager.getConnection(dbURL);
              
        } catch (Exception e) {
            e.printStackTrace();           
        }
        
    }
   private static void selectAll()
    {
        try
        {
            stmt = conn.createStatement();
            ResultSet results = stmt.executeQuery(query);
            ResultSetMetaData rsmd = results.getMetaData();
          
            while(results.next())
            {
                String envName = results.getString(1);
                String aplName = results.getString(2);
                String aplVer =  results.getString(3);
                String depName = results.getString(4);
                String depVer = results.getString(5);
                System.out.println(envName + "|" +aplName+ "|"+ aplVer+ "|" + depName+ "|" +depVer + "|");
            }
            results.close();
            stmt.close();
        }
        catch (SQLException sqlExcept)
        {
            sqlExcept.printStackTrace();
        }
    }
    
}
