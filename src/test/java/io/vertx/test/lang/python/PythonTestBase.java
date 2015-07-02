package io.vertx.test.lang.python;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;

/**
 * @author <a href="http://tfox.org">Tim Fox</a>
 */
public abstract class PythonTestBase {

  protected String getMethodName() {
    return Thread.currentThread().getStackTrace()[3].getMethodName();
  }

  protected abstract String getTestFile();

  protected void runTest() throws Exception {
    PythonRunner runner = new PythonRunner();
    runner.start_gateway();
    try {
      TimeUnit.MILLISECONDS.sleep(2000);
    } catch (InterruptedException ex) { }
    String path = "src/test/resources/" + getTestFile();
    runner.run(path, getMethodName());
  }
}
