/*
 * Sample test module to exercize the -fstack-protector buffer overflow
 * detection feature.
 *
 * Author:	Nicolas Pitre
 * Created:	June 7, 2010
 * Copyright:	Canonical Ltd
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 *
 * Beware: upon insertion of this module, the kernel should panic!
 */

#include <linux/kernel.h>
#include <linux/module.h>

static long (*test_fn)(long *);

static long test_good(long *x)
{
	int i;
	long v;

	x[0] = 0;
	x[1] = 1;
	for (i = 2; i < 50; i++) {
		v = x[i-1] + x[i-2];
		x[i] = v;
	}

	return v;
}

static void test_bad_target(void)
{
	/* Execution should never get here. */
	panic("*** FAIL: STACK OVERFLOW DETECTION DID NOT TRIGGER ***\n");
}

static long test_stack_attack(long *x)
{
	int i;

	/*
	 * Let's overwrite the stack to scrub over our caller's
	 * own return address.
	 */
	for (i = 50; i < 70; i++)
		x[i] = (long)&test_bad_target;

	/*
	 * And then pretend some normality.
	 */
	return test_good(x);
}

/* this is not marked "static" to make sure it is not inlined */
long test_stackprotected_caller(long *x)
{
	long buffer[50];
	return test_fn(buffer);
}

static int __init test_stackprotector_init(void)
{
	long dummy_buffer[20];

	printk(KERN_CRIT "*** stack protector test module ***\n");

	test_fn = &test_good;
	printk(KERN_CRIT "... testing normal function call\n");
	test_stackprotected_caller(dummy_buffer);

	test_fn = &test_stack_attack;
	printk(KERN_CRIT "... testing rogue function call\n");
	test_stackprotected_caller(dummy_buffer);

	/* the kernel should have panicked by now */
	printk(KERN_CRIT "*** FAIL: stack overflow attempt did not work ***\n");
	return -EINVAL;
}

module_init(test_stackprotector_init)
MODULE_LICENSE("GPL");
