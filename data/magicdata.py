import os
import csv
import pandas
import fnmatch

base_path = '/project/student_projects3/yzhu/data/magicdata'


def generate_trn(data_path):
    print('Entering {} ...'.format(data_path))
    transcripts = pandas.read_csv(os.path.join(data_path, 'TRANS.txt'), sep='\t', index_col=0)

    wav_path = [os.path.join(dirpath, f)
                for dirpath, dirnames, files in os.walk(data_path)
                for f in fnmatch.filter(files, '*.wav')]

    for wav in wav_path:
        trn = os.path.splitext(wav)[0] + '.trn'
        print("genearting trn files for {}".format(trn))
        with open(trn, 'w') as ftrn:
            wav_name = os.path.basename(wav)
            ftrn.write(transcripts.loc[wav_name, 'Transcription'])


def generate_csv(data_path):
    train_path = os.path.join(data_path, 'train')

    train_wav_paths = [os.path.join(dirpath, f)
                        for dirpath, dirnames, files in os.walk(train_path)
                        for f in fnmatch.filter(files, '*.wav')]

    train_transcript_path = list(map(lambda wav_path : wav_path + '.trn',
                                     train_wav_paths))

    with open('train_manifest_magicdata.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(train_wav_paths)):
            writer.writerow([train_wav_paths[i], train_transcript_path[i]])
    
    
    dev_path = os.path.join(data_path, 'dev')

    dev_wav_paths = [os.path.join(dirpath, f)
                        for dirpath, dirnames, files in os.walk(dev_path)
                        for f in fnmatch.filter(files, '*.wav')]

    dev_transcript_path = list(map(lambda wav_path : wav_path + '.trn',
                                     dev_wav_paths))

    with open('dev_manifest_magicdata.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(dev_wav_paths)):
            writer.writerow([dev_wav_paths[i], dev_transcript_path[i]])
    
    
    test_path = os.path.join(data_path, 'test')

    test_wav_paths = [os.path.join(dirpath, f)
                        for dirpath, dirnames, files in os.walk(test_path)
                        for f in fnmatch.filter(files, '*.wav')]

    test_transcript_path = list(map(lambda wav_path : wav_path + '.trn',
                                     test_wav_paths))

    with open('test_manifest_magicdata.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(test_wav_paths)):
            writer.writerow([test_wav_paths[i], test_transcript_path[i]])


def process(dataset_path):
    print('starting to process {}'.format(dataset_path))
    for subset in ['train', 'test', 'dev']:
        subset_path = os.path.join(dataset_path, subset)
        generate_trn(subset_path)

    generate_csv(dataset_path)


if __name__ == '__main__':
    process(base_path)
