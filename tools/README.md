# Tools Documentation
* [json_generator.py](#json_generator.py)
* [parse_mutations.py](#parse_mutations.py)
* [make_autograder](#make_autograder)

# json_generator.py
This python script is a helper to generate informational results.json output in the proper Gradescope format. The ideal use is that several results.json files are generated throughout the autograder's run and then they are combined at the very end. These are created with a score of 0/1 or 0/0 only.

**NOTE**: This script does not write to files. We pipe to a file in shell for that functionality.

Arguments:
* `--title <string>`: Result title
* `--body <string>`: Result body
* `--input <filepath>`: Input file to read as results body instead of --body
* `--passtest`: Grade the test as 0/0 (passing). If not set, the grade will be 0/1
* `--combine <dir>`: Combine all the json files in a specified folder and produce a single combined output

Example usage:
```bash
# Missing directory
python3 json_generator.py --title "Missing src/main" > results4.json

# A test that failed with compiler output
python3 json_generator.py --title "Student code compiles" --input /tmp/compile.out > results5.json

# A test that passed
python3 json_generator.py --title "Student code compiles" --passtest > results6.json

# Combine results at the end of script
python3 json_generator.py --combine /autograder/results > /autograder/results/results.json
```


# parse_mutations.py
This python script is a helper to find and convert the mutation results csv to proper Gradescope json output file.

**NOTE**: This script DOES write to a file (unlike json_generator)

Arguments:
* `--reportpath`: Directory for pit-reports. ex: `test_staging/target/pit-reports`
* `--max_points`: Maximum points for the testing portion of assignment, divided among mutants
* `--output`: Json file to output
* `--verbose`: Include specific details for the results of each mutation. If not set, student will just see mutations killed out of total mutations.

Example usage:
```bash
# Convert mutation results
python3 parse_mutations.py --reportpath /autograder/source/staging_test/target/pit-results --maxpoints 50 --verbose --output results7.json
```


# make_autograder
This script cleans unnecessary files and prepares an `Autograder.zip` to upload to Gradescope. The following files get erased:
* *.DS_Store
* staging_main/src/main/*
* staging_main/target/
* staging_test/src/*
* staging_test/target/
* Potentially others, TODO: Update this to be exact


# make_dynamic_autograder

This script creates a version of the autograder that is connected to this private repository, so that you don't have to reupload the `Autograder.zip` file more than once.
It's based heavily on the [link-gs-zip-with-repo](https://github.com/ucsb-gradescope-tools/link-gs-zip-with-repo) utility that Phill Conrad's team created. The only difference is that it's entirely tuned to this repository.

If you are making minor changes to your assignment, you do NOT need to update the `Autograder.zip` file on Gradescope.  You only update your private repo.

It works, because the scripts are set up to do a "git pull" from your private repo before each student's submission is graded.

The only times you would need to regenerate the `Autograder.zip` are when:

1. If you change the packages you are installing in the `setup.sh` script.
2. If you have so many changes to so many files that the `git pull` is slowing down the grading.  In that case, 
   regenerating the `Autograder.zip` file is not strictly necessary, but may improve performance.

But, for simple changes, such as changing a test case, fixing a bug in the starter code, etc., you can simply change the code in the private repo for the assignment, push the change to github, and then the autograder just starts using your new version immediately.   Nice!

This whole thing is simply a way of automating and simplifying the process described [here](https://gradescope-autograders.readthedocs.io/en/latest/git_pull/) in Gradescope's own documentation.  If you want to get down and dirty under the hood, read that.  If you just want it to work with minimum effort, read on.

Instructions are as follows:

1. Prepare this repo as you normally would, creating your testing scripts in `staging_main/`.
2. Run ./tools/make_deploy_keys.sh to generate a public/private key pair.  You can
   run this anywhere (e.g. on any system that has `ssh-keygen` and a Unix shell).
   
   * *private key:* `deploy_keys/deploy_key`
   * *public key:* `deploy_keys/deploy_key.pub`

   Note that these two files are in the `.gitignore` and should generally
   NOT be uploaded to a git repo.  The private key becomes part of the `Autograder.zip`
   file, while the public key gets attached to the github repo as it's "deploy key":
   
3. Upload the public key (`deploy_keys/deploy_key.pub`) as the deploy key for your assignment specific github repo, following [these instructions](https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys). The script should suggest you to do this after you run it in Step 2.

6. Run `./tools/make_dynamic_autograder_zip` (although the step 2 script should also ask if you want to do this).

7. Use the generated `Autograder.zip` file as the thing you upload to Gradescope.

8. For small changes, only update the github repo.

9. For big changes, redo the `./tools/make_dynamic_autograder_zip` script, and reupload the `Autograder.zip` file.