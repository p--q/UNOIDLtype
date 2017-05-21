import step2createRDB
import step3createXCUs
import step4createManifest
import step5createOXT
import step6depoyOXT
if __name__ == '__main__':
    # シェルコマンドのエラーでは止まらないのでログを最初から確認する必要あり。
    print("\nstep2\n")
    step2createRDB.main()
#     print("\nstep3\n")
#     step3createXCUs.main()
    print("\nstep4\n")
    step4createManifest.main()
    print("\nstep5\n")
    step5createOXT.main()
    print("\nstep6\n")
    step6depoyOXT.main()
