from vertx_python.core import vertx

def main():
    def cb1(cv, uh):
        print("got clustered vertx {}".format(cv))
        print("got huh {}".format(uh))

        def cb2(c, uh):
            print("got huh {}".format(uh))
            print("got c {}".format(c))
        cv.shared_data().get_cluster_wide_map("mymap", cb2)

    vertx.Vertx.clustered_vertx(cb1)

if __name__ == "__main__":
    main()
