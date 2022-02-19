import argparse

from trainer import OCRTrainer


def non_or_str(value):
    if value == None:
        return None
    return value

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='OCR using CNN+RNN+CTC')
    
    parser.add_argument('--resume', type=non_or_str, help='resume from a checkpoint')
    
    parser.add_argument('--dataset', type=non_or_str, default="./dataset", help='dataset for training/evaluation')
    
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    
    parser.add_argument('--lr', type=float, default=0.001, help='Learning Rate')
    
    parser.add_argument('--eval', default=False, action='store_true', help='perform evaluation of trained model for display')
    
    parser.add_argument('--eval_chords', default=False, action='store_true', help='perform evaluation of trained model for accuracy')
    
    # batch mode: where the batch size is equal to the total dataset thus making the iteration and epoch values equivalent
    # mini-batch mode: where the batch size is greater than one but less than the total dataset size. Usually, a number that can be divided into the total dataset size.
    # stochastic mode: where the batch size is equal to one. Therefore the gradient and the neural network parameters are updated after each sample.
    parser.add_argument('--batch_size', type=int, default=1) # https://github.com/tensorflow/tensorflow/issues/40919#issuecomment-653776885
    
    parser.add_argument('--interval', type=int, default=150)
    
    # To evaluate a single image
    parser.add_argument('--eval_img', type=non_or_str, help='Predict on single image')
    
    args = parser.parse_args()    

    trainer = OCRTrainer(args)

    if args.eval:
        trainer.eval()
    elif args.eval_chords:
        trainer.eval_chords()
    elif args.eval_img is not None:
        trainer.eval_img(args.eval_img)
    else:
        trainer.train()

# python3 main.py --dataset ./dataset I am not using pipenv in the mac !
# python3 main.py --resume ./checkpoint/best.h5 --eval_img './dataset/E minor.png'
