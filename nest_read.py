#!/usr/bin/env python

import click
import arrow
from dotenv import load_dotenv

from sensor_lib.thermostat import Thermostat
from settings import Settings
from nest_lib import NestAPI

load_dotenv()

@click.group(chain=True)
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)
    config = Settings()
    api = NestAPI(config)
    ctx.obj["settings"] = config
    ctx.obj["api"] = api

@cli.command("thermostat")
@click.option("-d", "--device_id",
              required=False,
              metavar="DEVICEID",
              envvar="THERMOSTAT_DEVICE_ID")
@click.pass_context
def thermostat(ctx, device_id):
    ctx.obj["device_id"] = device_id
    api: NestAPI = ctx.obj["api"]
    thermo = api.get_device_detail(device_id)
    ctx.obj["thermostat"] = thermo

@cli.command("stdout")
@click.option("-t", "--time-format",
              "time_format",
              default=arrow.FORMAT_RSS)
@click.pass_context
def stdout(ctx, time_format):
    if isinstance(ctx.obj["thermostat"], Thermostat):
        thermo: Thermostat = ctx.obj["thermostat"]
        now = arrow.get(thermo.time_received).to('local').format(time_format)
        data = [
            f"{now} thermo.ambient.temp:{round(thermo.ambient_temp, 2)}",
            f"{now} thermo.ambient.humidity:{thermo.ambient_humidity}",
            f"{now} thermo.hvac.mode:{thermo.mode}",
            f"{now} thermo.hvac.status:{thermo.status}",
            f"{now} thermo.hvac.setpoint:{round(thermo.setpoint_per_settings, 0)}",
        ]
        for dat in data:
            click.echo(dat)

if __name__ == "__main__":
    cli()
