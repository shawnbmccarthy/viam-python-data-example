import argparse
import asyncio
import sys

from datetime import datetime as dt, timedelta as td
from logging import Logger

from viam.app.data_client import DataClient
from viam.app.viam_client import ViamClient
from viam.logging import getLogger
from viam.proto.app.data import CaptureInterval, Filter
from viam.rpc.dial import DialOptions
from viam.utils import datetime_to_timestamp

logger: Logger = getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='viam data viewer'
    )
    parser.add_argument('--organization', '-o', type=str, required=True)
    parser.add_argument('--api-key', '-a', type=str, required=True)
    parser.add_argument('--api-id', '-i', type=str, required=True)
    parser.add_argument('--start', '-s', type=str, required=True)
    parser.add_argument('--end', '-e', type=str, required=True)
    parser.add_argument('--location', '-l', type=str, required=False)
    parser.add_argument('--component', '-c', type=str, required=False)
    parser.add_argument('--component-type', '-t', type=str, required=False)
    # add other filters here?

    return parser.parse_args()


async def main(args: argparse.Namespace) -> None:
    start = dt.fromisoformat(args.start)
    end = dt.fromisoformat(args.end)
    org_id = args.organization
    api_key = args.api_key
    api_id = args.api_id
    component = args.component
    location = args.location

    viam_client: ViamClient = await ViamClient.create_from_dial_options(
        DialOptions.with_api_key(api_key=api_key, api_key_id=api_id),
        app_url='https://app.viam.com:443'
    )
    data_client: DataClient = viam_client.data_client

    capture_interval: CaptureInterval = CaptureInterval(
        start=datetime_to_timestamp(start),
        end=datetime_to_timestamp(end)
    )

    f: Filter = Filter(
        component_name=component,
        organization_ids=[org_id],
        interval=capture_interval
    )

    td = await data_client.tabular_data_by_filter(filter=f)
    count = 0
    sz = 0
    for i in td:
        count += 1
        sz += sys.getsizeof(i)
    viam_client.close()

    print(f'{count} records for: {end - start} time period')
    print(f'{sz} of all records (bytes)')
    print(f'avg size (bytes): {sz/count}')


if __name__ == "__main__":
    asyncio.run(main(parse_args()))
