package io.vertx.test.lang.python;

import java.io.File;
import java.net.URL;
import java.lang.ProcessBuilder.Redirect;
import java.net.InetAddress;
import java.io.IOException;

import io.vertx.core.Vertx;

import py4j.GatewayServer;

/**
 * @author <a href="http://tfox.org">Tim Fox</a>
 */
public class PythonRunner {

  private GatewayServer gateway;
  private int port = 25333;
  private int client_port = 24333;
  private Process Process;

  public static void main(String[] args) {
  }

  public Vertx getVertx() {
    return Vertx.vertx();
  }

  public void start_gateway() throws Exception {
    if (gateway == null) {
      boolean connected = false;
      while (!connected) {
        try {
          gateway = new GatewayServer(new PythonRunner(), port, client_port,
                                      InetAddress.getByName(GatewayServer.DEFAULT_ADDRESS),
                                      InetAddress.getByName(GatewayServer.DEFAULT_ADDRESS),
                                      GatewayServer.DEFAULT_CONNECT_TIMEOUT,
                                      GatewayServer.DEFAULT_READ_TIMEOUT,
                                      null
                                      );
          gateway.start();
          connected = true;
        } catch (Exception e) {
          port++;
          client_port++;
        }
        if (port > 25440) {
          throw new Exception("Failed to bind to port");
        }
      }
    }
  }

  public int run(String scriptName, String testName) throws Exception {
    return run(scriptName, testName, true, true);
  }

  public int run(String scriptName, String testName, boolean provideRequire, 
                 boolean provideConsole) throws Exception {
    ProcessBuilder pb = new ProcessBuilder("python", "-u", scriptName, 
                                           String.valueOf(port), 
                                           String.valueOf(client_port), 
                                           testName);
    pb.redirectOutput(Redirect.INHERIT);
    pb.redirectError(Redirect.INHERIT);
    Process process = pb.start();
    int out = process.waitFor();
    gateway.shutdown();
    gateway = null;
    return out;
      
  }
}
