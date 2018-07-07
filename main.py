PRODUCTION = True

if PRODUCTION:
    from run import main
    main()
else:
    from testing import main
    main()
