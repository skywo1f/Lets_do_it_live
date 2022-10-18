/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "hardware/dma.h"

#define LED_PIN 25

#define P_PIN 4
#define M_PIN 5

#define POL_PIN 6
#define SHORTPOL_PIN 7
#define TENABLE_PIN 8
#define SHORTRECV_PIN 9
#define RENABLE_PIN 10
#define CAPTURE_CHANNEL 0
#define CAPTURE_DEPTH 1000

#define DEBUG false
uint8_t capture_buf[CAPTURE_DEPTH];

volatile bool timer_fired = false;

//single atoi
int sAtoI(char c){
	int num = c - '0';
	return num;
}

//take in the message in 5 digit csv
bool parseMessage(char *buffer, int *timings) {
        bool noMessage = true;
	if(DEBUG) printf("received %s \n",buffer);
        if (buffer[5] == ',' ){
                noMessage = false;

                for (int i = 0; i < 14; i++)
                {
                       timings[i] += sAtoI(buffer[i*6 + 0])*10000;
                       timings[i] += sAtoI(buffer[i*6 + 1])*1000;
                       timings[i] += sAtoI(buffer[i*6 + 2])*100;
                       timings[i] += sAtoI(buffer[i*6 + 3])*10;
                       timings[i] += sAtoI(buffer[i*6 + 4])*1;
                }
		if (DEBUG) printf("\n %d \n",timings[5]);
        }
        return noMessage;
}

int64_t send_signal_callback(alarm_id_t id,int totalTime) {
//        printf("sending signal \n");
//	gpio_init(P_PIN);
//        gpio_set_dir(P_PIN, GPIO_OUT);
//        gpio_init(M_PIN);
//        gpio_set_dir(M_PIN, GPIO_OUT);

	int longDelay = 2*totalTime/5;
        int shortDelay = totalTime/10;
//	printf("long delay: %d \n short delay: %d \n",longDelay,shortDelay);
	for (int i = 0; i < 4; i++){
	        gpio_put(P_PIN,1);
	        busy_wait_us(longDelay);
	        gpio_put(P_PIN,0);
	        busy_wait_us(shortDelay);
	        gpio_put(M_PIN,1);
	        busy_wait_us(longDelay);
	        gpio_put(M_PIN,0);
	        busy_wait_us(shortDelay);
	}
	return 0;
}

int64_t start_adc_callback(alarm_id_t id,int endTime) {
  gpio_init(LED_PIN);
  gpio_set_dir(LED_PIN, GPIO_OUT);

	gpio_put(LED_PIN, 1);
	if (DEBUG) printf("starting dma adc \n");
	adc_gpio_init(26 + CAPTURE_CHANNEL);        //set up to listen from the first gpio  
	adc_init();                                 //init gpio 26
	adc_select_input(CAPTURE_CHANNEL); 
	adc_fifo_setup(
    		true,    // Write each completed conversion to the sample FIFO
	    	true,    // Enable DMA data request (DREQ)
	    	1,       // DREQ (and IRQ) asserted when at least 1 sample present
	    	false,   // We won't see the ERR bit because of 8 bit reads; disable.
	    	true     // Shift each sample to 8 bits when pushing to FIFO
	);                                          //set it up for fifo
	
	adc_set_clkdiv(0);       //do this as fast as possible
	busy_wait_us(1000000);        //not sure if you actually have to wait
	uint dma_chan = dma_claim_unused_channel(true);     //declare a channel for dma access
    	dma_channel_config cfg = dma_channel_get_default_config(dma_chan);//set up the dma access
	channel_config_set_transfer_data_size(&cfg, DMA_SIZE_8); //more details for dma channel
	channel_config_set_read_increment(&cfg, false); //adc register doesnt move
	channel_config_set_write_increment(&cfg, true); //record to an array of data
	channel_config_set_dreq(&cfg, DREQ_ADC);//when to actually do a transfer(when adc does)
	    dma_channel_configure(dma_chan, &cfg,
	        capture_buf,    // dst
	        &adc_hw->fifo,  // src
	        CAPTURE_DEPTH,  // transfer count
	        true            // start immediately
	    );  //start now, stop after 1000 samples
	adc_run(true);              //go!
	dma_channel_wait_for_finish_blocking(dma_chan);//solves the problem of race condition
	adc_run(false); //stop recording adc when dma finishes
	adc_fifo_drain();//get rid of any extra adc data that didnt get transferred from the fifo
	gpio_put(LED_PIN, 0);

    	// Print samples to stdout so you can display them in pyplot, excel, matlab
    for (int i = 0; i < CAPTURE_DEPTH; ++i) {//print out the data
        printf("%-3d %d \n", capture_buf[i],i);
	
	if (i % 1000 == 999)
            printf("\n");
    }
}

int64_t start_pol_callback(alarm_id_t id,void *user_data) {
	if (DEBUG) printf("starting polarization\n");
	gpio_init(POL_PIN);
        gpio_set_dir(POL_PIN, GPIO_OUT);

	gpio_put(POL_PIN,1);
}

int64_t end_pol_callback(alarm_id_t id,void *user_data) {
	if (DEBUG) printf("ending polarization \n");
        gpio_put(POL_PIN,0);
}

int64_t last_callback(alarm_id_t id, void *user_data) {
	timer_fired = true;
	return 0;
}

void setAlarms(int *timings) {
	if (DEBUG) printf("setting alarms \n");
        gpio_init(P_PIN);
        gpio_set_dir(P_PIN, GPIO_OUT);
        gpio_init(M_PIN);
        gpio_set_dir(M_PIN, GPIO_OUT);

//prepare send signal
//	add_alarm_in_ms(timings[0],send_signal_callback,timings[1],true);
//prepare adc
        add_alarm_in_ms(timings[12],start_adc_callback,timings[13],true);
//start polarization
//        add_alarm_in_ms(timings[2],start_pol_callback,NULL,true);

//end polarization
//	add_alarm_in_ms(timings[3],end_pol_callback,NULL,true);
//end timer
//	add_alarm_in_ms(10000,last_callback,NULL,true);
}

void runRelays(int *timings){
	gpio_init(SHORTPOL_PIN);
	gpio_set_dir(SHORTPOL_PIN, GPIO_OUT);
	gpio_init(TENABLE_PIN);
	gpio_set_dir(TENABLE_PIN, GPIO_OUT);
	gpio_init(SHORTRECV_PIN);
	gpio_set_dir(SHORTRECV_PIN, GPIO_OUT);
	gpio_init(RENABLE_PIN);
	gpio_set_dir(RENABLE_PIN, GPIO_OUT);

	int shortPol_triggered = 0;
	int tEnable_triggered = 0;
	int shortRecv_triggered = 0;
	int rEnable_triggered = 0;
	if (DEBUG) printf("starting relays\n");
	while(1){
//short polarizer coil
	if (time_us_64() > 1000*timings[4] && shortPol_triggered == 0)	{
		shortPol_triggered = 1;
		gpio_put(SHORTPOL_PIN,1);
		if (DEBUG) printf("pol coil short\n");		
	}
	if (time_us_64() > 1000*timings[5] && shortPol_triggered == 1) {
		shortPol_triggered = 2;
		gpio_put(SHORTPOL_PIN,0);
	}
//enable transmitter
	if (time_us_64() > 1000*timings[6] && tEnable_triggered == 0)       {
                tEnable_triggered = 1;
                gpio_put(TENABLE_PIN,1);
		if (DEBUG) printf("transmitter enable\n");
        }
        if (time_us_64() > 1000*timings[7] && tEnable_triggered == 1) {
                tEnable_triggered = 2;
                gpio_put(TENABLE_PIN,0);
        }
//short receiver coil
	if (time_us_64() > 1000*timings[8] && shortRecv_triggered == 0)       {
                shortRecv_triggered = 1;
                gpio_put(SHORTRECV_PIN,1);
		if (DEBUG) printf("receiver coil short \n");
        }
	if (time_us_64() > 1000*timings[9] && shortRecv_triggered == 1) {
                shortRecv_triggered = 2;
                gpio_put(SHORTRECV_PIN,0);
        }
//enable receiver connection to end of circuit
	if (time_us_64() > 1000*timings[10] && rEnable_triggered == 0)       {
                rEnable_triggered = 1;
                gpio_put(RENABLE_PIN,1);
		if (DEBUG) printf("receiver coil enable \n");
        }
        if (time_us_64() > 1000*timings[11] && rEnable_triggered == 1) {
                rEnable_triggered = 2;
                gpio_put(RENABLE_PIN,0);
        }
	}

}

int main() {
	stdio_init_all();
        bool noMessage = true;
        char buffer[1024];
	if (DEBUG) printf("starting up\n");
//1 wave initializer
//1 polarize coil enable
//4 relays
//1 adc
//4 is short pol
//6 is transmit enable
//8 is short receiver
//10 is receiver enable
//
        int timings[14] = {2,500,4,5,6,7,8,12,8,9,6,15,4000,200};
//wait for message
/*	while (noMessage) {
                scanf("%1024s", buffer);
                noMessage = parseMessage(buffer,timings);
        }
	for (int i = 0; i < 14; i++ ) {
		printf("%d ",timings[i]);
	}
*/
	setAlarms(timings);
//	runRelays(timings);	

	//in case it finishes relays before the timers fired
    	while (!timer_fired) {
        	tight_loop_contents();
    	}
}
