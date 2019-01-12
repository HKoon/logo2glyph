package FontSwitchBackend.Controller;

import net.sf.json.JSONArray;

import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import org.apache.commons.codec.binary.Base64;

@RestController
@RequestMapping(value="/api")
public class FontSwitchController {

    @PostMapping(value="/switch")
    @ResponseBody
    public JSONArray getSwitchPic(@RequestParam("typepicname")String typepicname, @RequestParam("content")String content){
        System.out.println(typepicname);
        System.out.println(content);
        String stylePath = "./style/"+ typepicname;
        String contentPath = "./abc/"+content+".png";
        try {
            System.out.println("start");
            String[] args1=new String[]{"python","g2g_simple.py",stylePath,contentPath};
            Process pr=Runtime.getRuntime().exec(args1);
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    pr.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            pr.waitFor();
            System.out.println("end");
        } catch (Exception e) {
            e.printStackTrace();
        }

        InputStream in = null;
        byte[] data = null;
        try
        {
            in = new FileInputStream("./images/output.png");
            data = new byte[in.available()];
            in.read(data);
            in.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        String img =  new String(Base64.encodeBase64(data));

        in = null;
        data = null;
        try
        {
            in = new FileInputStream("./images/gen_img.png");
            data = new byte[in.available()];
            in.read(data);
            in.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        String cmp =  new String(Base64.encodeBase64(data));


        return JSONArray.fromObject("[{'pic':'"+img+"'},{'cmp':'"+cmp+"'}]");
    }


}