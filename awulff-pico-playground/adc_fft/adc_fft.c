// Sample from the ADC continuously at a particular sample rate
// and then compute an FFT over the data
//
// much of this code is from pico-examples/adc/dma_capture/dma_capture.c
// the rest is written by Alex Wulff (www.AlexWulff.com)

#include <stdio.h>
#include <math.h>

#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/dma.h"
#include "kiss_fftr.h"

// set this to determine sample rate
// 0     = 500,000 Hz
// 960   = 50,000 Hz
// 9600  = 5,000 Hz

int fScale = 5;
#define CLOCK_DIV 48000/fScale
#define FSAMP 1000*fScale
//#define CLOCK_DIV 960     		//default
//#define CLOCK_DIV 4800			//10hz div
//#define CLOCK_DIV 9600			//5hz div
//#define CLOCK_DIV 48000			//1hz div
//#define FSAMP 50000			//default
//#define FSAMP 10000			//10hz div
//#define FSAMP 5000			//5hz div
//#define FSAMP 1000			//1hz div

// Channel 0 is GPIO26
#define CAPTURE_CHANNEL 0
#define LED_PIN 25

// BE CAREFUL: anything over about 9000 here will cause things
// to silently break. The code will compile and upload, but due
// to memory issues nothing will work properly

#define NSAMP 1000 //default

// globals
dma_channel_config cfg;
uint dma_chan;
float freqs[NSAMP];
void setup();
void sample(uint8_t *capture_buf);

int main() {
  uint8_t cap_buf[NSAMP];
  kiss_fft_scalar fft_in[NSAMP*fScale]; // kiss_fft_scalar is a float
  float powers[NSAMP*fScale];
//  kiss_fft_cpx fft_out[NSAMP];
  kiss_fft_cpx fft_out[NSAMP*fScale];
  kiss_fftr_cfg cfg = kiss_fftr_alloc(NSAMP*fScale,false,0,0);
  
  // setup ports and outputs
  setup();

  while (1) {
    // get NSAMP samples at FSAMP
    sample(cap_buf);
    // fill fourier transform input while subtracting DC component
    uint64_t sum = 0;
    float avg = (float)sum/(float)NSAMP;

    for (int i=0;i<NSAMP;i++) {fft_in[i]=((float)cap_buf[i]);}
//    for (int i=0;i<NSAMP;i++) {fft_in[i]=((float)cap_buf[i]-avg);} //default
    for(int i = 0; i < NSAMP*(fScale - 1); i++) {fft_in[i+NSAMP] = 0;}	//fill the rest with 0's

    // compute fast fourier transform
    kiss_fftr(cfg , fft_in, fft_out);
    
    // compute power and calculate max freq component
    float max_power = 0;
    int max_idx = 0;
    // any frequency bin over NSAMP/2 is aliased (nyquist sampling theorum)
    for (int i = 0; i < NSAMP/2; i++) {
      float power = fft_out[i].r*fft_out[i].r+fft_out[i].i*fft_out[i].i;
/*
        if (i == 94){			//get rid of 97hz noise
		power = power - 1300;
	}
	if (i == 95) {
		power = power - 34000;
	}
	if (i == 96) {
		power = power - 60000;
	}
	if (i == 97) { 
		power = power - 76000;
	}
	if (i == 98) {
		power = power - 72000;
	}
	if (i == 99){
		power = power - 50000;
	}
	if (i == 100) {
		power = power - 24000;
	}
*/
	if (i < 35 || i > 400){ //get rid of power outside of bass range
		power = 0;
	}
		

      powers[i] = power;
/*
      if (power>max_power) {
	max_power=power;
	max_idx = i;
      }
*/
    }
    /*
	if (powers[(int)max_idx/2]  > 5000){ //if subharmonic exists, thats probably the note being played
	max_power = powers[max_idx] + powers[(int)max_idx/2];
        max_idx = (int)max_idx/2;
	}
*/
int maxima[NSAMP/2];		//list of maximum frequencies above cutoff
	int maxCounter = 0;
	int cutoff = 10000;
	for (int i = 30; i < NSAMP/2 - 1; i++) {
		if (powers[i] > cutoff) {
			if (powers[i] > powers[i - 1] && powers[i] > powers[i + 1]){
				maxima[maxCounter] = i;
				maxCounter++;
			}
		}
	}
	int multCounter[NSAMP/2];	//list of how many mult counters each max frequency has
	for(int i = 0; i < maxCounter ; i++){
		multCounter[i] = 0;
		for (int j = i; j < maxCounter; j++){
			if (maxima[j]%maxima[i] < 2 || maxima[j]%maxima[i] > maxima[i] - 2) {
				multCounter[i]++;
			}
		}
	}
	max_idx = 0;
	int max_counter = 0;
	float max_freq;
	for(int i = 0; i < maxCounter; i++){
		if (multCounter[i] > max_counter){
			max_counter = multCounter[i];
			max_freq = maxima[i];
		}	
	}
	int max_harm = max_counter;
//    float max_freq = freqs[max_idx];
/*
    if (max_power > 1){
    printf("Greatest Frequency Component: %0.1f Hz @ % 0.1f power\n",max_freq,max_power);
    }
 */
   if(max_harm > 1){ 
    printf("Greatest Frequency Component: %0.1f Hz, with %d harmonics \n",max_freq,max_harm);
	}
    /* 
        for (int i = 0; i < 500; i++){
	printf("%f ", powers[i]);
    } 
    printf("\n");
*/
//    printf("%f \n" ,avg);

    }

  // should never get here
  kiss_fft_free(cfg);
}

void sample(uint8_t *capture_buf) {
  adc_fifo_drain();
  adc_run(false);
      
  dma_channel_configure(dma_chan, &cfg,
			capture_buf,    // dst
			&adc_hw->fifo,  // src
			NSAMP,          // transfer count
			true            // start immediately
			);

  gpio_put(LED_PIN, 1);
  adc_run(true);
  dma_channel_wait_for_finish_blocking(dma_chan);
  gpio_put(LED_PIN, 0);
}

void setup() {
  stdio_init_all();

  gpio_init(LED_PIN);
  gpio_set_dir(LED_PIN, GPIO_OUT);

  adc_gpio_init(26 + CAPTURE_CHANNEL);

  adc_init();
  adc_select_input(CAPTURE_CHANNEL);
  adc_fifo_setup(
		 true,    // Write each completed conversion to the sample FIFO
		 true,    // Enable DMA data request (DREQ)
		 1,       // DREQ (and IRQ) asserted when at least 1 sample present
		 false,   // We won't see the ERR bit because of 8 bit reads; disable.
		 true     // Shift each sample to 8 bits when pushing to FIFO
		 );

  // set sample rate
  adc_set_clkdiv(CLOCK_DIV);

  sleep_ms(1000);
  // Set up the DMA to start transferring data as soon as it appears in FIFO
  uint dma_chan = dma_claim_unused_channel(true);
  cfg = dma_channel_get_default_config(dma_chan);

  // Reading from constant address, writing to incrementing byte addresses
  channel_config_set_transfer_data_size(&cfg, DMA_SIZE_8);
  channel_config_set_read_increment(&cfg, false);
  channel_config_set_write_increment(&cfg, true);

  // Pace transfers based on availability of ADC samples
  channel_config_set_dreq(&cfg, DREQ_ADC);

  // calculate frequencies of each bin
  float f_max = FSAMP;
  float f_res = f_max / NSAMP;
  for (int i = 0; i < NSAMP; i++) {freqs[i] = f_res*i;}
}
