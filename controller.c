/*
 * ATRAS | ADELANTE, Theta +|-
 * IZQUIERDA | DERECHA, Phi +|-
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <math.h>
#include "util/type.h"
#include "util/util.h"
#include "attitude/attitude.h"
#include "controller.h"

/*float integrate(float integral, float val, float ant, double dt)
{
	integral += dt * (val + ant)/2;
	return integral;
}*/
float sign(float x)
{
	if(x<0) return -1;
	else if(x==0) return 0;
	else return 1;
}
void updatexd(super_twisting *st, PID *pid, float hd, float thd, float phd, float psd)
{
}
void updateatt_u(super_twisting *c, float th, float thp, float ph, float php, float ps, float psp)
{
	float tmp; 
	float l = 0.13, Ixx = 24.1e-3, Iyy = 23.2e-3, Izz = 45.1e-2;
        float b = 0.000006646195542576290, d = b*9.72;
        float ginvth = Ixx/l, ginvph = Iyy/l, ginvps = Izz;
	c->dt = util_timestamp() - c->ta;
	c->ta = util_timestamp();
	c->th = th;
	c->ph = ph;
	c->ps = ps;
	c->eth = c->thd - c->th;
	c->eph = c->phd - c->ph;
	c->eps = c->psd - c->ps;
	c->epth = c->thpd - thp;
	c->epph = c->phpd - php;
	c->epps = c->pspd - psp;

	tmp = c->epth + c->lambda*c->eth;	// s
	c->intsgnth += c->dt * (sign(tmp) + sign(c->sth))/2; // Integrate
	c->sth = tmp;
        tmp = c->epph + c->lambda*c->eph;	// s
        c->intsgnph += c->dt * (sign(tmp) + sign(c->sph))/2; // Integrate
        c->sph = tmp;
        tmp = c->epps + c->lambda*c->eps;	// s
        c->intsgnps += c->dt * (sign(tmp) + sign(c->sps))/2; // Integrate
        c->sps = tmp;
        printf("e= %.3f %.3f %.3f\n",c->eth, c->eph, c->eps); //Imprime el error
	printf("\nxp= %.3f %.3f %.3f\n",thp, php, psp); // Imprime la derivada
	c->uth = c->lambda * c->epth - c->K1 * sqrt(fabs(c->sth)) * sign(c->sth) - c->K2 * c->intsgnth;
	c->uth = ginvth * c->uth;

        c->uph = c->lambda * c->epph - c->K1 * sqrt(fabs(c->sph)) * sign(c->sph) - c->K2 * c->intsgnph;
        c->uph = ginvph * c->uph;

        c->ups = c->lambda * c->epps - c->K1 * sqrt(fabs(c->sps)) * sign(c->sps) - c->K2 * c->intsgnps;
        c->ups = ginvps * c->ups;
//	printf("u= %.3f %.3f %.3f\n",c->uth,c->uph,c->ups);

}
void updatealt_u(PID *c, float alt)
{
	float P, e, m = 0.42, g = 9.78;
        c->dt = util_timestamp() - c->ta;
        c->ta = util_timestamp();
	e = c->xd - alt;
	P = e;
        c->I += c->dt * (e + c->eant)/2; // Integrate
	if(e - c->eant == 0)
	{
		c->n++;
	} else {
		c->D =  (e - c->eant)/c->dt/c->n;
		c->n = 1;
	}
	c->eant = e;
	c->ualt = c->kp * P + c->ki * c->I + c->kd * c->D;
	// Se le suma m*g para contrarrestar el peso del cuadricoptero
	// para que el controlador solo tenga que estabilizarlo en un punto
	c->ualt += m * g; 

	if(c->ualt < 0) c->ualt = 0;
}
int init_controller(super_twisting *st, PID *pid)
{
	st->uth = 0;
	st->uph = 0;
	st->ups = 0;
	printf("Introduce la ganancia K1 : ");
	scanf("%f",&st->K1);
	printf("K1 = %f\n",st->K1);
	printf("Introduce la ganancia K2: ");
	scanf("%f",&st->K2);
	printf("K2 = %f\n",st->K2);
	st->th = 0;
	st->ph = 0;
	st->ps = 0;
	st->thd = 0;
	st->phd = 0;
	st->psd = 0;
	st->thpd = 0;
	st->phpd = 0;
	st->pspd = 0;
	printf("Introduce la ganancia lambda: ");
	scanf("%f",&st->lambda);
	st->intsgnth = 0;
	st->intsgnph = 0;
	st->intsgnps = 0;
	st->antth = 0;
	st->antph = 0;
	st->antps = 0;
	st->dt = 1;
	st->ta = util_timestamp();
	pid->ualt = 0;
	printf("Introduce la ganancia kp: ");
	scanf("%f",&pid->kp);
	printf("Introduce la ganancia ki: ");
	scanf("%f",&pid->ki);
	printf("Introduce la ganancia kd: ");
	scanf("%f",&pid->kd);
	pid->I = 0;
	pid->D = 0;
	printf("Introduce la altura deseada: ");
	scanf("%f",&pid->xd);
	pid->eant = 0;
	pid->n = 1;
	pid->dt = 1;
	pid->ta = st->ta;
	return 0;
}
